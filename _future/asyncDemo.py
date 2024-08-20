import asyncio

async def toast_bread():
  print("Starting to toast bread")
  await asyncio.sleep(5)  # Simulates toasting
  print("Bread is ready!")

async def boil_water():
  print("Starting to boil water")
  await asyncio.sleep(8)  # Simulates boiling
  print("Water is boiling!")

async def main():
  task1 = asyncio.create_task(toast_bread())
  task2 = asyncio.create_task(boil_water())
  await task1
  await task2

async def main2():
    toast_bread()
    boil_water()

#asyncio.run(main2())
asyncio.run(main())
