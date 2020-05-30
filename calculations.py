day = 28#int(input("Ingrese el dia\n"))
month = 11#int(input("Ingrese el mes\n"))
year = 2015#int(input("Ingrese el año\n"))
longitude = '74º25\'8"W'#input('Ingrese la longitud\n')
localHour = '20h15m30s'#input('Ingrese la hora local\n')

def dms2dec(coordinate):

    #eliminacion de caracteres especiales
    conversion = coordinate.replace('º'," ").replace('\''," ").replace('\"', " ").split()

    #conversion de coordenada en grados, minutos, segundos a formato punto flotante
    degrees = float(conversion[0])+float(conversion[1])/60+float(conversion[2])/3600

    #Correcion de coordenada segun hemisferio
    if conversion[3] == "S" or conversion[3] == 'W':
        degrees *= -1

    return degrees

def hms2hour(hms):

    conversion = hms.replace('h'," ").replace('m'," ").replace('s', " ").split()
    hour = float(conversion[0]) + float(conversion[1])/60 + float(conversion[2])/3600

    return hour

def tiempoUniversal (TSOLM, longitude):

    longitude = dms2dec(longitude)
    TU = hms2hour(TSOLM) + longitude/15 if longitude>0 else hms2hour(TSOLM) - longitude/15

    return TU

def fechaJuliana (day, month, year):
    year = year - 1 if (month == 1 or month == 2) else year
    month = month + 12 if (month == 1 or month == 2) else month

    julianDate = int(365.25*(year + 4716)) + int(30.6001*(month + 1)) - int(year/100) + int(int(year/100)/4) + day -1522.5

    return julianDate

def TSG0 (day, month, year):

    T = (fechaJuliana(day, month, year) - 2451545)/36525

    part1 = 6/24 + (41/60)/24 + (50.54841/3600)/24
    part2 = (2400/24 + (3/60)/24 + (4.81286/3600)/24)*T
    part3 = ((0.09310/3600)/24)*(T**2)

    tsg0 = (part1+part2+part3)*24
    return tsg0 if tsg0<24 else tsg0 - int(tsg0/24)*24

def TSL(day, month, year, position, TL):

    tsl = TSG0(day,month,year) + tiempoUniversal(TL ,position)*1.0027379
    tsl = tsl if tsl<24 else tsl-24
    finalCount = dms2dec(position)

    return tsl - finalCount/15 if finalCount > 0 else tsl + finalCount/15

print(TSL(day,month,year,longitude,localHour))
