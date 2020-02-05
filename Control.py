import pyvisa
import numpy as np
import pandas as pd
import time





def readdata(ch_number,my_instrument,yoff,yzero,ymult):             
    
    cmd = f'DATA:SOURCE CH{ch_number}'
    my_instrument.write(cmd)
    time.sleep(1.5)
    data = my_instrument.query_binary_values('CURVE?',datatype='h',container=np.array)
    data = (data -yoff) * ymult +yzero

    return data


def initialize(my_instrument,data_number):
   
    my_instrument.write('DATa:ENCdg SRIbinary')
    time.sleep(1)
    my_instrument.write('WFMOutpre:BYT_Nr 2')
    time.sleep(1)

    ymult = float(my_instrument.query('WFMOutpre:YMUlt?'))
    yzero = float(my_instrument.query("WFMOutpre:YZERO?"))
    yoff = float(my_instrument.query('WFMOutpre:YOFF?'))
    my_instrument.write('Data:START 1')
    my_instrument.write(f'Data:STop {data_number}')
    
 

    return my_instrument,{'ymult':ymult,'yzero':yzero,'yoff':yoff}

def save_waveforme_tocsv(filename):
    try:
        import time
        import visa as pyvisa
        rm = pyvisa.ResourceManager()
        my_instrument = rm.open_resource(rm.list_resources()[0])
        my_instrument,param = initialize(my_instrument,40000)
        stop = 'ACQuire:STATE STOP'
        run = 'ACQuire:STATE RUN'

        x0,x1 = my_instrument.write(stop)
        time.sleep(1)
        ch1 = readdata(1,my_instrument,**param)

        ch2 = readdata(2,my_instrument,**param)

        ch3 = readdata(3,my_instrument,**param)
        ch4 = readdata(4,my_instrument,**param)
        import pandas as pd
        dataframe = pd.DataFrame(dict(ch1=ch1,ch2=ch2,ch3=ch3,ch4=ch4))
        dataframe.to_csv(filename,index=None)

        x0,x1 = my_instrument.write(run)
    finally:
        my_instrument.close()
        rm.close()

if __name__ == '__main__':
    for i in range(10):
        save_waveforme_tocsv(f'{i}')
        time.sleep(5)
    import winsound
    winsound.Beep(500,1000)





