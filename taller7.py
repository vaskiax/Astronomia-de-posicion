day = 8 #int(input("Ingrese el dia\n"))
month = 5#int(input("Ingrese el mes\n"))
year = 2010#int(input("Ingrese el año\n"))
longitude = '7h30m0s'#input('Ingrese la longitud\n')
latitude = '65h12m0s'#int(input('Ingrese la latitud del lugar\n'))
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

def dec2dms(lat):

        #Parsear las coordenadas en formato grados, minutos, segundos
        latitude = []

        #conversion de punto flotante a formato dms
        latitude.append(str(int(lat/15))+'h')
        inter = abs((lat-int(lat)))*60
        latitude.append(str(int((inter)))+"m")
        inter2 = (inter - int(inter))*60
        latitude.append(str(int(inter2))+"s")


        latitude = latitude[0]+" "+latitude[1]+" "+latitude[2]+' '

        return latitude

def toHourAngle(degree):
    degrees = degree
    ent2 = abs((degrees - int(degrees))*60)
    ent3 = abs((ent2 - int(ent2))*60)
    declination = str(int(degrees))+'º'+str(int(ent2))+'´'+str(int(ent3))+'\"'

    return declination

def radians(angle):
    from numpy import pi
    radian = (angle*pi)/180
    return radian

def degrees(radian):
    from numpy import pi
    degree = (radian*180)/pi
    return degree

def hms2hour(hms):

    conversion = hms.replace('h'," ").replace('m'," ").replace('s', " ").split()
    hour = float(conversion[0]) + float(conversion[1])/60 + float(conversion[2])/3600

    return hour

def hour2hms(lat):
    #Parsear las coordenadas en formato grados, minutos, segundos
    latitude = []

    #conversion de punto flotante a formato dms
    latitude.append(str(int(lat/15))+'h')
    inter = abs((lat-int(lat)))*60
    latitude.append(str(int((inter)))+"m")
    inter2 = (inter - int(inter))*60
    latitude.append(str(int(inter2))+"s")


    latitude = latitude[0]+" "+latitude[1]+" "+latitude[2]+' '

    return latitude

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

def MandN(day, month, year):

    T = (fechaJuliana(day, month, year) - 2451545)/36525
    m1 = dms2dec('1.2812323º0.00001\'0.0001\"N')*T
    m2 = dms2dec('0.003879º0.00001\'0.00001\"N')*T**2
    m3 = dms2dec('0.0001101º0.00001\'0.00001\"N')*T**3

    n1 = dms2dec('0.5567530º0.00001\'0.00001\"N')*T
    n2 = dms2dec('0.001185º0.00001\'0.00001\"N')*T**2
    n3 = dms2dec('0.000116º0.00001\'0.00001\"N')*T**3

    M = m1+m2+m3
    N = n1-n2-n3

    return M,N,T

def dateTransform(day, month, year, ra, dec):
    from numpy import sin, cos, tan

    MN = MandN(day, month, year)
    ra = hms2hour(ra)
    dec = hms2hour(dec)
    ram = ra + (MN[0] + MN[1]*sin(radians(ra))*tan(radians(dec)))*0.5 + 90
    decm = dec + MN[1]*cos(radians(ram))*0.5

    rightAscension = ra + MN[0] + MN[1]*sin(radians(ram))*tan(radians(decm)) +90
    declination = dec + MN[1]*cos(radians(ram))

    return rightAscension, declination, ram, decm

def moonData(day, month, year):

    T = (fechaJuliana(day, month, year) - 2451545)/36525

    herradura = 125.4 - 1934.13*T
    D = 297.85 + 445267.11*T
    D = 360*((D/(360))-int(D/(360)))
    F = 93.27 + 483202.0175*T
    F = 360*((F/(360))-int(F/(360)))
    E = dms2dec('23º26\'21.4\"N') - dms2dec('0º0\'46.81\"N')*T
    E = 360*((E/(360))-int(E/(360)))

    return radians(herradura), radians(D), radians(F), radians(E)

def nutation(day, month, year, rightAscension, declination):

    from numpy import sin, cos, tan

    moonDatas = moonData(day, month, year)
    coordinates = dateTransform(day, month, year, rightAscension, declination)
    ra = radians(coordinates[0])
    dec = radians(coordinates[1])

    deltaY = -hms2hour('0h0m17.2s')*sin(moonDatas[0]) \
    + hms2hour('0h0m0.2s')*sin(2*moonDatas[0]) \
    - (-hms2hour('0h0m1.3s')*sin(2*moonDatas[0]+2*moonDatas[2]-2*moonDatas[1])) \
    - hms2hour('0h0m0.2s')*sin(2*moonDatas[0]+2*moonDatas[2])

    deltaE = hms2hour('0h0m9.2s')*cos(moonDatas[0]) \
    -(-hms2hour('0h0m0.1s')*cos(moonDatas[0])) \
    + hms2hour('0h0m0.6s')*cos(2*moonDatas[0]+2*moonDatas[2]-2*moonDatas[1])
    + hms2hour('0h0m9.2s')*cos(2*moonDatas[0]+2*moonDatas[2])

    deltaRa = (cos(moonDatas[3])+sin(moonDatas[3])*sin(ra)*tan(dec))*deltaY - cos(ra)*tan(dec)*deltaE
    deltaDec = sin(moonDatas[3])*cos(ra)*deltaY + sin(ra)*deltaE

    trueRa = hour2hms(hms2hour(rightAscension)+deltaRa+90)
    trueDec = toHourAngle(hms2hour(declination)+deltaDec)
    trueE = moonDatas[3]+deltaE

    return trueRa, trueDec, trueE, deltaRa, deltaDec, toHourAngle(degrees(moonDatas[3]))


print(nutation(day, month, year, longitude, latitude),sep='\n')
