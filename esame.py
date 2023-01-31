class ExamException(Exception):
    pass

class CSVTimeSeriesFile():

    def __init__(self, name):
        if not isinstance(name, str):
            raise ExamException('il nome non è una stringa')
        self.name=name

    def get_data(self):
        try:
            open_file=open(self.name,'r')
        except:
            raise ExamException('file non leggibile')
        lista_di_liste=[]
        counter=0
        for line in open_file:
            if counter!=0:
                elements=line.split(',')
                try:
                    elements[0]=int(float(elements[0]))
                    elements[1]=float(elements[1])
                    elements_0e1=[]
                    elements_0e1.append(elements[0])
                    elements_0e1.append(elements[1])
                    lista_di_liste.append(elements_0e1)
                except:
                    pass
                        
            counter+=1
        if len(lista_di_liste)==0:
            raise ExamException('la lista è vuota')
        count=0
        for line in lista_di_liste:
            if count>0:
                if line[0]<=lista_di_liste[count-1][0]:
                    raise ExamException('timestamp non ordinati')
            count+=1
        return lista_di_liste

def compute_daily_max_difference(time_series):
    try:
        lista_differenze=[]
        min=None
        max=None
        ep_in_giorno_line_preced=None
        for line in time_series:
            epoch_inizio_giorno=line[0]-(line[0]%86400)
            if epoch_inizio_giorno!=ep_in_giorno_line_preced:
            #se è il primo dato del giorno
                min=line[1] #ri-setto la max e min aggiornate al giorno
                max=line[1]
                lista_differenze.append(None)
            else:
            # se è la seconada o più misurazione di un giorno
                if line[1]>max:
                    max=line[1]
                if line[1]<min:
                    min=line[1]
                differenza=max-min
                lista_differenze.pop(-1) #elimino il None messo dalla prima misurazione del giorno o la differenza messa dalla misurazione precedente
                lista_differenze.append(differenza)
            #(print(max,min,max*min,lista_differenze[-1]))
            ep_in_giorno_line_preced=epoch_inizio_giorno
        
        return lista_differenze

    except:
        raise ExamException('errori nella funzione compute')


time_series_file = CSVTimeSeriesFile('data.csv')
time_series = time_series_file.get_data()
listadidifferenze=compute_daily_max_difference(time_series)
print(listadidifferenze)