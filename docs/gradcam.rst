gradcam
================

This library 

.. code-block:: python

    class GradCAM:
        def __init__(self, model=None, layer_name=""):
            print("init gradcam")
            print(model)
            self.model = model

            self.layer_name = layer_name
            if layer_name!="":
                self.layer_name = layer_name
                try:
                    layer=self.model.get_layer(self.layer_name)
                except Exception as e:
                    print(f"Error getting the layer: {e}", "reverting to last convolutional layer")
                    self.layer_name = ""
            
            if self.layer_name=="" and self.model is not None:
                for layer in reversed(self.model.layers):
                    if isinstance(layer, tf.keras.layers.Conv2D):
                        self.layer_name = layer.name
                        break
            

            if self.layer_name == "":
                print("Error finding the last convolutional layer")
            
            print("layer name:",self.layer_name)

            try:
                self.grad_model = tf.keras.models.Model([self.model.inputs], [self.model.get_layer(self.layer_name).output, self.model.output])
            except Exception as e:
                print(f"Error getting the model: {e}")
                self.grad_model = None
                
        def get_heatmap(self, path_to_image, pred_index=None):
            print("getting heatmap")
            print(self.grad_model)
            if self.grad_model is None:
                return None
            
            input_shape=self.model.input_shape[1:]
            print("input shape",input_shape)
            print("reading image:",path_to_image)
            image = cv2.imread(path_to_image, cv2.IMREAD_COLOR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = image.astype('float32')
            image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)
            tensor = tf.convert_to_tensor(image)
            tensor = np.expand_dims(tensor, axis=0)
            print("post tensor")
            with tf.GradientTape() as tape:
                last_conv_layer_output, preds = self.grad_model(tensor)            
                if pred_index is None:
                    pred_index = tf.argmax(preds[0])
                class_channel = preds[:, pred_index]

            

            grads = tape.gradient(class_channel, last_conv_layer_output)
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            last_conv_layer_output = last_conv_layer_output[0]
            heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
            
            heatmap_rgb = cm.coolwarm(heatmap)[:, :, :3] * 255
            heatmap_rgb = heatmap_rgb.astype('uint8')
            heatmap = cv2.resize(heatmap_rgb, (tensor.shape[2], tensor.shape[1]))
            
            print(preds)
            print(pred_index)
            return heatmap, preds, pred_index
        
        # add in a mysqldb connection to put the heatmap into the database
        def insert_into_runtime(self, path_to_image, plot_type_id, model_id, runnum=0):

            dbhost = 'hallddb.jlab.org'
            dbname = 'hydra'
            dbuser = 'aimon'
            dbcnx=MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
            dbcursor=dbcnx.cursor(MySQLdb.cursors.DictCursor)
            
            
            img_pth_parse=path_to_image.split("/")
            fileName_full=img_pth_parse[-1].split(".")[0]

            print("filename=",fileName_full)
            
            with open(path_to_image, 'rb') as f:
                plot_img = base64.b64encode(f.read())
            
            gradCAMheatmap=None
            if model_id!=-1:
                gradCAMheatmap, preds, top_class_index = self.get_heatmap(path_to_image)
            
            encoded_gradcam=b""

            
            if gradCAMheatmap is None:
                print("no gradcam heatmap can be made")
                encoded_gradcam=b""
            else:

                heatmap_bytes = np.uint8(255 * gradCAMheatmap)
                _, imgbuffer = cv2.imencode('.png', heatmap_bytes)

                encoded_gradcam=base64.b64encode(imgbuffer)
            
            top_class="NoModel"
            VerdictConfidence=1.0
            if model_id!=-1:
                labels_query = "SELECT Labels FROM Models WHERE ID = "+str(model_id)
                print(labels_query)
                dbcursor.execute(labels_query)
                res=dbcursor.fetchall()
                labels=ast.literal_eval(str(res[0]["Labels"],"utf-8")) #this is our normal labels dictionary now
                print(labels)
                print(top_class_index.numpy())
                top_class = labels[top_class_index.numpy()] #this is the top class label (i.e. Good, Bad, etc.)
                print(top_class)
                print(list(preds.numpy()[0])[top_class_index.numpy()])
                VerdictConfidence=list(preds.numpy()[0])[top_class_index.numpy()]

            insert_str = "INSERT into RunTime (HydraHostName,DateTime,BeamCurrent,RunNumber,PlotType_ID,PlotName,IMG,gradCAM,ModelID,VerdictLabel,VerdictConfidence,Confirmed, PlotTime) VALUES (\"test\",NOW(),100,"+str(runnum)+","+str(plot_type_id)+",\""+fileName_full+"\",\""+str(plot_img,"utf-8")+"\",\""+str(encoded_gradcam,"utf-8")+"\","+str(model_id)+",\""+str(top_class)+"\","+str(VerdictConfidence)+",1,NOW())"
            dbcursor.execute(insert_str)
            dbcnx.commit()
            dbcnx.close()
