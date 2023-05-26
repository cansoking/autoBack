# %%
import tensorflow as tf
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


# %% 构建模型
def create_model():
    model = Sequential([
        layers.experimental.preprocessing.Rescaling(1. / 255, input_shape=(24, 24, 1)),
        layers.Conv2D(24, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(96, activation='relu'),
        layers.Dense(15)]
    )

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    return model


# %% 预测
def predict(model, imgs, class_name):
    label_dict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '=', 11: '+',
                  12: '-', 13: '×', 14: '÷'}
    # 预测图片，获取预测值
    predicts = model.predict(imgs)
    results = []  # 保存结果的数组
    for single in predicts:  # 遍历每一个预测结果
        index = np.argmax(single)  # 寻找最大值
        result = class_name[index]  # 取出字符
        results.append(label_dict[int(result)])
    return results
