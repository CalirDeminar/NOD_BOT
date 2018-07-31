import FuelTracker
ft = FuelTracker.FuelTracker()

ft.update_structure("astra", 20)
ft.update_structure("fort", 50)


ft.update_structure("athanor", 10)

print(ft.list_structures())
#print(ft.fuel_status())
