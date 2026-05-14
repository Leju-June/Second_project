import keras

# keras MNIST 데이터셋 로드
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
# 60000개의 이미지,라벨 데이터와 10000개의 테스트데이터를 튜플로 불러옴

# 데이터 스케일링 (0~255 -> 0~1)
x_train = x_train / 255.0
x_test = x_test / 255.0

# One-Hot Encoding
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)
# 정답이 [0,2,1] 이면 [[1,0,0..], [0,0,1..], [0,1,0..]] 로 변환 (예시)

# MLP 모델 아키텍쳐 생성
BATCH_SIZE = 64
EPOCHS = 16

class MLP():
	def __init__(self):
		self.model = keras.models.Sequential([
			keras.layers.Flatten(input_shape=[28,28]),
			# Flatten : 28x28 -> 784개의 1차원 배열로 변환
			keras.layers.Dense(512, activation="relu"),
			keras.layers.Dense(256, activation="relu"),
			keras.layers.Dropout(0.2),
			keras.layers.Dense(10, activation="softmax")
		])

# 모델 컴파일
mlp_model = MLP()
mlp_model.model.compile(
	optimizer='adam',
	loss='categorical_crossentropy',
	metrics=['accuracy']
)

# 모델 학습 및 평가
mlp_model.model.fit(
	x_train, y_train,
	BATCH_SIZE,
	EPOCHS,
	validation_split=0.2,
)

mlp_model.model.evaluate(x_test, y_test)

# 모델 저장
mlp_model.model.save("mlp_model_v1.h5")

print("모델이 성공적으로 저장되었습니다: mlp_model_v1.h5")