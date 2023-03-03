x = ['Fisher + Chris Lake', "Pi'erre Bourne", 'Horsegirl', 'Soul Glo', 'DPR LIVE + DPR IAN', 'Desert Cahuilla Bird Singers', 'Eric Prydz Presents HOLO', 'Pusha T', 'Sasha + John Digweed', 'DJ Tennis & Carlita', 'Momma', '2manydjs', 'Eladio Carrión', 'Dennis Cruz + PAWSA', 'Dinner Party ft. Terrace Martin, Robert Glasper, Kamasi Washington', '1999.ODDS', 'Saba', "Donavan's Yard"]
x_new = []
for i in x:
    if " + " in i:
        i = i.split(" + ")
        x_new.append(i[0])
        x_new.append(i[1])
    else:
        x_new.append(i)

print(x_new)