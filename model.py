from keras.models import Model, Sequential
from keras.layers import Input, Conv2D, MaxPool2D, Flatten, Dropout, Dense, BatchNormalization, Activation, MaxPooling2D
from keras.utils.vis_utils import plot_model

import numpy as np
import keras, glob, random,json
from keras import backend as K
from keras.models import model_from_json
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical
from scipy import misc
from keras.datasets import mnist
from keras.utils import np_utils
from PIL import Image, ImageFilter, ImageEnhance
from keras.callbacks import TensorBoard,ModelCheckpoint
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.layers import Input, Dense, Dropout
from keras.models import Model

train_data = glob.glob("NCT-CRC-HE-100K/*/*.tif") #the glob module is used to retrieve files/pathnames matching a specified pattern.

test_data = glob.glob("CRC-VAL-HE-7K/*/*.tif") 

target_name =  ["ADI","BACK","DEB","LYM","MUC","MUS","NORM","STR","TUM"]
filepath = "best_weights.h5"
checkpoint =ModelCheckpoint(filepath, monitor='accuracy', verbose=0, save_best_only=True, mode='max', period=1)  #to save a model or weights (in a checkpoint file) at some interval, so the model or weights can be loaded later to continue the training from the state saved.to only keep the model that has achieved the "best performance"
random.shuffle(train_data)
random.shuffle(test_data)
import cv2  # is a library of programming functions 
from keras.utils import Sequence
import math


class SequenceData(Sequence):
    def __init__(self, batch_size, target_size,data):
        # 初始化所需的参数

        self.batch_size = batch_size
        self.target_size = target_size
        self.x_filenames = data

    def __len__(self):
        # 让代码知道这个序列的长度
        num_imgs = len(self.x_filenames)
        return math.ceil(num_imgs / self.batch_size)

    def __getitem__(self, idx):
        # 迭代器部分
        batch_x = self.x_filenames[idx * self.batch_size: (idx + 1) * self.batch_size]
        imgs = []
        y = []
        for x in batch_x:
            img = Image.open(x)
            
            img =img
 
            imgs.append(img)
            y.append(target_name.index(x.split("\\")[-2]))
            
        x_arrays = 1 - np.array([np.array(i) for i in imgs]).astype(
            float) / 255  # 读取一批图片

 
        batch_y = to_categorical( np.array(y) , 9)
         

        return x_arrays, batch_y


batch_size =10
steps = math. ceil(len(train_data) / batch_size)
target_size =(224, 224)
test_steps = math. ceil(len(test_data) / batch_size)
sequence_data = SequenceData(batch_size, target_size,train_data)

sequence_test_data = SequenceData(batch_size, target_size,test_data)
class TrainCNNModel:

    def build(self):
        """建立模型  模型样式如下

        """

        img_size = (224, 224,3)  # 全体图片都resize成这个尺寸
        input_image = Input(shape=(img_size[0], img_size[1], 3))
        base_model = ResNet50( input_tensor=input_image,weights='imagenet', include_top=False, pooling='svg' )
        x = Flatten()(base_model.output)
        outputs = Dense(9, activation='softmax')(x) 

        self.model = Model(inputs=input_image, outputs=outputs)
        
        print('\n')

        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        return self.model

    def reload_model(self):
        """重新载入模型  可载入之前的已训练过的模型继续训练  也可载入模型后让模型做识别图片工作"""
        print("开始重新载入模型:ResNet50.model")
        self.model = model_from_json(open('ResNet50.json').read())

        self.model.load_weights('ResNet50.model')
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])  ##编译 网络

        return self.model

    def train(self):
        print("开始训练模型....")
        for layer in self.model.layers:
            layer.trainable = False
        
        for x in range(10): ## 开放最后20层为可训练

            self.model.layers[-x].trainable = True
      
        for x in self.model.trainable_weights:
            print(x.name,"可训练")

        history = self.model.fit_generator(sequence_data, steps_per_epoch=steps, epochs=30, verbose=1,
       
						initial_epoch=0,
        callbacks=[TensorBoard(log_dir='./logs/'),checkpoint],# 设置日志存放目录
        validation_data=sequence_test_data,validation_steps=test_steps
                                           
                                        )
        self.model.save_weights("ResNet50.model")  ## 保存模型权重
        with open('ResNet50.json', 'w') as f:
            f.write(self.model.to_json())  ## 保存模型网络
        return history

    def evaluate(self):  ##测试计算准确率
       

        score = self.model.evaluate(sequence_test_data , verbose=1)
        print('测试 正确率:', score)  ##正确率
    def orc_img(self, cropImg):
        """ 识别图片"""
        img = 1 -np.array(cropImg).astype(float)/ 255
        print(img.shape)
        predict = self.model.predict(np.array([img,]))
        index = predict.argmax()
        print("CNN预测",index,predict)
        
        target = target_name[index]
        index2 = np.argsort(predict)[0][-2]	
        target2 = target_name[index2] 
       


        return {"target": target, "predict": "%.2f" % (float(list(predict)[0][index]/sum(list(predict)[0])) * 100),	
   
                "target2": target2,
                "predict2": "%.2f" % (float(list(predict)[0][index2]/sum(list(predict)[0])) * 100),
               
            
                
                }

if __name__ == "__main__":
    t = TrainCNNModel()
    t.build()  ## 建立模型
    t.reload_model()  ## 重新载入之前已训练的模型
    t.model.summary()

    history = t.train()  ## 训练模型
    
    t.evaluate()  ##评估模型