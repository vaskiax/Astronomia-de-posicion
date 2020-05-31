day = 17 #int(input("Ingrese el dia\n"))
month = 3#int(input("Ingrese el mes\n"))
year = 2020#int(input("Ingrese el año\n"))
longitude = '75º33\'49"W'#input('Ingrese la longitud\n')
localHour = '0h0m0s'#input('Ingrese la hora local\n')

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

def sunCoordinates(day, month, year):

    from numpy import sin, cos, arcsin, arctan, pi, arange

    numberOfDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    sunVelocity = 360/365.25
    dayList = [range(1, i+1) for i in numberOfDays]
    days = []
    for i in dayList:
        days.append(list(i))

    months = days[3:month-1] if month > 3 else days[:2]
    cumDays = sum([len(i) for i in months]) + day if month > 3 else sum([len(i) for i in months]) - day
    cumDays = cumDays if month < 3 else cumDays + 12

    if month == 3:
        cumDays = abs(19-day)
    if month == 2:
        cumDays = 47
    if month == 1:
        cumDays = 47 + (31-day)


    angle = sunVelocity*cumDays
    firstEclipticLon = 360*((angle/(360))-int(angle/(360)))
    eclipticLat = 0
    finalEclipticLon = 0
    ecliptic = (23.27*pi)/180

    if year == 2020:
        if month < 3:
            finalEclipticLon = firstEclipticLon
        elif month == 3:
            if day < 19:
                finalEclipticLon = 360 - firstEclipticLon
            else:
                finalEclipticLon = firstEclipticLon
        else:
            finalEclipticLon = firstEclipticLon
    elif year < 2020:
        finalEclipticLon = 360 - firstEclipticLon
    else:
        finalEclipticLon = firstEclipticLon

    finalEclipticLon = (finalEclipticLon*pi)/180
    ra1 = -sin(eclipticLat)*sin(ecliptic)+cos(eclipticLat)*cos(ecliptic)*sin(finalEclipticLon)
    ra2 = cos(finalEclipticLon)*cos(eclipticLat)
    rightAscension = abs((arctan(ra1/ra2)*180)/pi) if month > 3 else 360 - abs((arctan(ra1/ra2)*180)/pi)

    declination = abs((arcsin(sin(eclipticLat)*cos(ecliptic)+cos(eclipticLat)*sin(ecliptic)*sin(finalEclipticLon))*180)/pi)

    return rightAscension, declination


print(sunCoordinates(day,month,year))
