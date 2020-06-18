day = 8 #int(input("Ingrese el dia\n"))
month = 5#int(input("Ingrese el mes\n"))
year = 2010#int(input("Ingrese el año\n"))
longitude = '7h30m0s'#input('Ingrese la longitud\n')
latitude = '65h12m0s'#int(input('Ingrese la latitud del lugar\n'))
localHour = '0h0m0s'#input('Ingrese la hora local\n')
longitud = '359º17\'44"N'
latitud = '17º35\'37"N'
"""
Funciones para realizar conversiones, algunas se repitieron con pequeños cambios
para no afectar otras funciones previamente creadas pero no debe tenerse en cuenta

"""
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
    declination = str(int(degrees))+'º'+str(int(ent2))+"´"+str(int(ent3))+'\"'

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

def hmstodec(hms):
    conversion = hms.replace('h'," ").replace('m'," ").replace('s', " ").split()
    hour = (float(conversion[0]) + float(conversion[1])/60 + float(conversion[2])/3600)*15
    return hour

def dectohms(lat):
    latitude = []

    #conversion de punto flotante a formato dms
    latitude.append(str(int(lat/15))+'h')
    inter = abs((lat-int(lat)))*60
    latitude.append(str(int((inter)))+"m")
    inter2 = (inter - int(inter))*60
    latitude.append(str(int(inter2))+"s")


    latitude = latitude[0]+" "+latitude[1]+" "+latitude[2]+' '

    return latitude

def hour2hms(lat):
    #Parsear las coordenadas en formato grados, minutos, segundos
    latitude = []

    #conversion de punto flotante a formato dms
    latitude.append(str(int(lat))+'h')
    inter = abs((lat-int(lat)))*60
    latitude.append(str(int((inter)))+"m")
    inter2 = (inter - int(inter))*60
    latitude.append(str(int(inter2))+"s")


    latitude = latitude[0]+" "+latitude[1]+" "+latitude[2]+' '

    return latitude
"""
Estas ya las había creado con anterioridad y para el caso de este taller
solo se hizo uso de la funcion fechaJuliana

"""
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
"""
Estas son las funciones usadas para el desarrollo de los puntos del taller 7:

la funcion passedTime fue especifica para el punto numero 6 dado que en este
se realizaron transformaciones de coordenadas y ademas las fechas no se ingresaron
como variables sino como valores fijos dentro de la funcion, por tanto, si se quiere
probar con fechas distintias en necesario modificar las entradas en la funcion

"""
def MandN(day, month, year):

    T = (fechaJuliana(day, month, year) - 2451545)/36525
    m1 = dms2dec('1.2812323º0\'0\"N')*T
    m2 = dms2dec('0.0003879º0\'0\"N')*T**2
    m3 = dms2dec('0.00001101º0\'0\"N')*T**3

    n1 = dms2dec('0.5567530º0\'0\"N')*T
    n2 = dms2dec('0.0001185º0\'0\"N')*T**2
    n3 = dms2dec('0.0000116º0\'0\"N')*T**3

    M = m1+m2+m3
    N = n1-n2-n3

    return M,N,T

def precesion(day, month, year, ra, dec, decDegree = False ,final=False):
    from numpy import sin, cos, tan

    MN = MandN(day, month, year)
    ra = hmstodec(ra)
    dec = hms2hour(dec) if decDegree==False else dec
    ram = ra + (MN[0] + MN[1]*sin(ra)*tan(dec))*0.5
    decm = dec + (MN[1]*cos(ram))*0.5

    rightAscension = ra + MN[0] + MN[1]*sin(ram)*tan(decm)
    declination = dec + MN[1]*cos(ram)

    return dectohms(rightAscension), declination if final==False else \
    toHourAngle(declination), ra, ram

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
    coordinates = precesion(day, month, year, rightAscension, declination)
    ra = radians(hmstodec(coordinates[0]))
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

    trueRa = dectohms(hmstodec(rightAscension)+deltaRa)
    trueDec = toHourAngle(hms2hour(declination)+deltaDec)
    trueE = moonDatas[3]+deltaE

    return trueRa, trueDec

def passedTime(day=1, month=1, year=2000,longitud, latitud):

    from astropy.coordinates import SkyCoord
    celestials = SkyCoord(str(dms2dec(longitud)),str(dms2dec(latitud)),\
    frame='geocentrictrueecliptic', unit='deg')

    celestials = celestials.transform_to('icrs')

    ra = celestials.ra.deg
    dec = celestials.dec.degree

    """
    Cambiar las fechas a las variables day, month, year en la funcion
    precesion para para hacer pruebas con otros valores si se desea.
    """
    years10 = precesion(1,1,2010,dectohms(ra),dec, decDegree=True)
    years100 = precesion(1,1,2100,dectohms(ra),dec, decDegree=True)

    coorYears10 = SkyCoord(str(hmstodec(years10[0])),\
    str(years10[1]),frame='icrs', unit='deg').transform_to('geocentrictrueecliptic')

    coorYears10 = toHourAngle(coorYears10.lon.degree),\
    toHourAngle(coorYears10.lat.degree)

    coorYears100 = SkyCoord(str(hmstodec(years100[0])),\
    str(years100[1]),frame='icrs', unit='deg').transform_to('geocentrictrueecliptic')

    coorYears100 = toHourAngle(coorYears100.lon.degree),\
    toHourAngle(coorYears100.lat.degree)

    return coorYears10, coorYears100


print(nutation(day, month, year, longitude, latitude),\
precesion(day,month,year,longitude,latitude, final=True),\
passedTime(longitud,latitud), sep='\n')
