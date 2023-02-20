import numpy as np
import matplotlib.pyplot as plt

antN=['(8,8)','(16,16)','(64,64)','(256,256)']
antNS=[240,1008,16368,262128]
antencop=[0.0133,0.0664,15.27,5134.615]
antencomrf=[0.0165,0.069,0.9998,16.8762]
plt.plot(antNS,antencomrf,label = 'MRF',color = 'green')
plt.xlabel('ADTMC States')
plt.ylabel('Encoding Time')
plt.legend()
plt.show()
plt.plot(antNS,antencop,label = 'Code',color = 'orange')
plt.xlabel('ADTMC States')
plt.ylabel('Encoding Time')
plt.legend()
plt.show()
airN=[10,100,1000,10000,100000]
airNS=[71,791,7991,79991,799991]
airencop=[0.0032,0.036,1.351,262.2,50460.889]
airencomrf=[0.0041,0.0412,0.3685,3.8421,39.7816]
plt.plot(airNS,airencop,label = 'MRF',color = 'green')
plt.xlabel('ADTMC States')
plt.ylabel('Encoding Time')
plt.legend()
plt.show()
plt.plot(airNS,airencomrf,label = 'Code',color = 'orange')
plt.xlabel('ADTMC States')
plt.ylabel('Encoding Time')
plt.legend()
plt.show()
brpN=[(4,2),(4,3),(16,2),(16,3),(16,4),(16,5),(32,2),(32,3),(32,4),(32,5),(64,2),(64,3),(64,4),(64,5),
      (64,8),(512,8),(2048,8)]
brpNS=[99,127,387,499,611,723,771,995,1219,1443,1539,1987,2435,2883,4227,33795,135171]
brpencop=[0.0028,0.0033,0.0101,0.0129,0.0187,0.0187,0.0201,0.0261,0.0327,0.0398,0.0430,0.0599,0.0790,0.0956,0.1862,4.594,148.4]
brpencomrf=[0.0035,0.0043,0.0122,0.015,0.0187,0.0222,0.0236,0.0299,0.0374,0.0442,0.0474,0.0613,0.0740,0.0876,0.1153,0.8733,3.649]
plt.plot(brpNS,brpencop,label = 'MRF',color = 'darkblue')
plt.xlabel('ADTMC States')
plt.ylabel('Encoding Time')
plt.legend()
plt.show()
plt.plot(brpNS,brpencomrf,label = 'Code',color = 'darkred')
plt.xlabel('ADTMC States')
plt.ylabel('Encoding Time')
plt.legend()
plt.show()
NSP=[10,26,240,1008,16368,262128,71,791,7991,79991,799991,99,127,387,499,611,723,771,995,1219,1443,1539,1987,2435,2883,4227,33795,135171]
NSM=[10,26,240,1008,16368,262128,71,791,7991,79991,799991,99,127,387,499,611,723,771,995,1219,1443,1539,1987,2435,2883,4227,33795,135171]
EncoP=[0.00075,0.00412,0.0133,0.0664,15.27,5134.615,0.0032,0.036,1.351,262.2,50460.889,0.0028,0.0033,0.0101,0.0129,0.0187,0.0187,0.0201,0.0261,0.0327,0.0398,0.0430,0.0599,0.0790,0.0956,0.1862,4.594,148.4]
EncoM=[0.00093,0.00188,0.0165,0.069,0.9998,16.8762,0.0041,0.0412,0.3685,3.8421,39.7816,0.0035,0.0043,0.0122,0.015,0.0187,0.0222,0.0236,0.0299,0.0374,0.0442,0.0474,0.0613,0.0740,0.0876,0.1153,0.8733,3.649]
print(len(NSP),len(NSM),len(EncoP),len(EncoM))
NSP=sorted(NSP)
NSM=sorted(NSM)
EncoP=sorted(EncoP)
EncoM=sorted(EncoM)
plt.plot(NSP,EncoP,label = 'Code',color = 'darkblue')
plt.xlabel('ADTMC States')
plt.ylabel('Encoding Time')
plt.legend()
plt.show()
plt.plot(NSM,EncoM,label = 'MRF',color = 'darkred')
plt.xlabel('ADTMC States')
plt.ylabel('Encoding Time')
plt.legend()
plt.show()
import numpy as np
slope, intercept = np.polyfit(np.log(NSP), np.log(EncoP), 1)
#print(slope)
plt.loglog(NSP, EncoP,label = 'Code', color='darkblue')
plt.legend()
plt.xlabel('log(|S|)')
plt.ylabel('log(Encoding-Time)')
plt.figtext(0.3, 0.65,'Slope=1.6')
plt.show()
slope, intercept = np.polyfit(np.log(NSP), np.log(EncoM), 1)
#print(slope)
plt.loglog(NSP, EncoM,label='MRF', color='darkred')
plt.legend()
plt.figtext(0.3, 0.65,'Slope=0.9775')
plt.xlabel('log(|S|)')
plt.ylabel('log(Encoding-Time)')
plt.show()

