#add to PhaseTenApp
async def run_app_task(self):  #This is the method that's gonna launch your kivy app
        await self.async_run(async_lib='asyncio')
        print('Kivy async app finished...')

    async def run_client_task(self): #Here you declare the other task
        print('Another task running inside the kivy loop')
        await run_main(self.client)


    # This func will start all the "tasks", in this case the only task is the kivy app
    async def base(self):
        (done, pending) = await asyncio.wait({self.run_app_task(), run_client_task()}, 
    return_when='FIRST_COMPLETED')


if __name__ == '__main__':
    p10 = PhaseTenApp() #You have to instanciate your App class
    asyncio.run(p10.base()) # Run in async mode




#-----------------------------------------
async def async_run(self, **kwargs):
    await super().async_run(**kwargs)
    # Additional asynchronous tasks can be started here



#-----------------------------------------
import asyncio 

######## MAIN APP ######## 
class PhaseTenApp(App):
    def build(self):
        #Your  app stuff here

    async def run_app_task(self):  #This is the method that's gonna launch your kivy app
        await self.async_run(async_lib='asyncio')
        print('Kivy async app finished...')

    # This func will start all the "tasks", in this case the only task is the kivy app
    async def base(self):
        (done, pending) = await asyncio.wait({self.run_app_task()}, 
    return_when='FIRST_COMPLETED')

if __name__ == '__main__':
    p10 = PhaseTenApp() #You have to instanciate your App class
    asyncio.run(instanciaApp.base()) # Run in async mode
'''
With the code above you'll be able to run tour kivy app as a task (concurrently).

So far, we just have run the kivy app in async mode (concurrently). To add other task inside the Kivy running loop:
'''

import asyncio 

######## MAIN APP ######## 
class PhaseTenApp(App):
    def build(self):
        #Your  app stuff here

    async def run_app_task(self):  #This is the method that's gonna launch your kivy app
        await self.async_run(async_lib='asyncio')
        print('Kivy async app finished...')

    async def task2InsideKivyLoop(self): #Here you declare the other task
        print('Another task running inside the kivy loop')
        await asyncio.sleep(1)


    # This func will start all the "tasks", in this case the only task is the kivy app
    async def base(self):
        (done, pending) = await asyncio.wait({self.run_app_task(), task2InsideKivyLoop()}, 
    return_when='FIRST_COMPLETED')

if __name__ == '__main__':
    p10 = PhaseTenApp() #You have to instanciate your App class
    asyncio.run(instanciaApp.base()) # Run in async mode
As you can see, to add another task inside the KivyLoop we just have to declare it as a async method of the App class, then just add it to asyncio.wait()

If you want to run the other task outside the kivyLoop you have to do the fllowing:

import asyncio 

######## MAIN APP ######## 
class PhaseTenApp(App):
    def build(self):
        #Your  app stuff here

    async def run_app_task(self):  #This is the method that's gonna launch your kivy app
        await self.async_run(async_lib='asyncio')
        print('Kivy async app finished...')

    # This func will start all the "tasks", in this case the only task is the kivy app
    async def base(self):
        (done, pending) = await asyncio.wait({self.run_app_task()}, 
    return_when='FIRST_COMPLETED')


######### GLOBAL COROUTINE #######
# Here you can import functions from other python files or just declare a global func
async def GlobalTask():
    for i in range(10):
        print('Other concurrently global task... ',i)
        await asyncio.sleep(1)
    await run_main(self.client)


if __name__ == '__main__':
        async def mainThread(): 
            p10 = PhaseTenApp() #Instanciate your App class
            a = asyncio.create_task(p10.base()) #Run kivyApp as a task
            b = asyncio.create_task(GlobalTask()) #Run Global func as a task
            (done, pending) = await asyncio.wait({a}, return_when='FIRST_COMPLETED')
    asyncio.run(mainThread())