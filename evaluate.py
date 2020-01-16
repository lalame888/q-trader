import keras
from keras.models import load_model
import h5py
from agent.agent import Agent
from functions import *
import sys
import os

if len(sys.argv) != 3:
	print ("Usage: python evaluate.py [stock] [model]")
	exit()

num_files=0
pathn = os.getcwd()
pathn+="/modelk" 
for fn in os.listdir(pathn):
        num_files += 1
mind = 0
maxd= 0	
batch_size = 32
pp=0
for k in range(13,14):
	stock_name, model_name = sys.argv[1], "model_ep"+str(k)+".h5"
	model = load_model("modelk/" + model_name)
	window_size = model.layers[0].input.shape.as_list()[1]-4
	agent = Agent(window_size, True, model_name)
	data = getStockDataVec(stock_name)
	mind = data[0]
	maxd = data[0]
	l = len(data) - 1
	agent.money = 1000000
	history=[]
	pp = np.mean(history) if history else float('nan')
	state = getState(data,0, window_size,maxd,mind,len(agent.inventory),agent.money/1000000,pp)
	total_profit = 0
	agent.inventory = []
	for t in range(l): 
		reward=0
		history.append(data[t])
		action = agent.act(state,data[t])
		# print(action)
		if data[t]>maxd:
			maxd = data[t]
		elif data[t]<mind:
			mind = data[t]
		# sit
		pp = np.mean(history) if history else float('nan')
		next_state = getState(data, t + 1, window_size,maxd,mind,len(agent.inventory),agent.money/1000000,pp)
		agent.inventory.sort()
		if action == 1:
			#print(np.mean(history))
			if len(agent.inventory) ==0:
				reward+=10
			agent.money -= data[t]
			agent.inventory.append(data[t]) 
			if data[t] < np.mean(history):
				reward+=(data[t]*(1/(np.mean(history)-mind)))	
			if len(agent.inventory)<10:
				reward+=5
			#print ("Buy: " + formatPrice(data[t]) + ", money: "+formatPrice(agent.money))

		elif action == 2 and len(agent.inventory) > 0: # sell
			#print(np.mean(history))
			agent.money += data[t]
			bought_price = agent.inventory.pop(0)
			reward = max((data[t] - bought_price),0)
			total_profit += (data[t] - bought_price)
			#print ("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
		elif action ==2 and len(agent.inventory) == 0:
			reward-=1
		elif action ==0:	
			reward-=1	
			#print("hold")
		#print("reward = ",reward)

		done = True if t == l - 1 else False
		agent.memory.append((state, action, reward, next_state, done))
		state = next_state

		if done:
			print ("--------------------------------")
			print ("Total Profit: " + formatPrice(total_profit))
			print ("--------------------------------")

		if len(agent.memory) > batch_size:
			agent.expReplay(batch_size)

