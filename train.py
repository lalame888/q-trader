from agent.agent import Agent
from functions import *
from keras.models import load_model
import sys
import numpy as np
import math
import h5py

if len(sys.argv) != 4:
	print("Usage: python train.py [stock] [window] [episodes]")
	exit()

# stock_name -> csv file name
# window_size -> day
flag = 0
stock_name, window_size, episode_count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
model_name = "model_ep50.h5"
model = load_model("modelk/" + model_name)
agent = Agent(window_size+4,True,model_name)
data = getStockDataVec(stock_name) # 每天的收盤價
l = len(data) - 1 # 資料總天數 2514
batch_size = 32 # ???
maxd= 0
mind = 0
hold_size = 0
for e in range(episode_count + 1):
	print ("Episode " + str(e) + "/" + str(episode_count))
	maxd = data[0]
	mind = data[0]
	history=[]
	pp = np.mean(history) if history else float('nan')
	state = getState(data, 0, window_size,maxd,mind,len(agent.inventory),agent.money/1000000,pp)
	total_profit = 0
	agent.money = 1000000
	agent.inventory = []
	
	for t in range(l): 
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
		reward = 0
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

	#if e%10==0 and e>=10:
	agent.model.save("./modelk/model_ep" + str(e+50)+".h5")
