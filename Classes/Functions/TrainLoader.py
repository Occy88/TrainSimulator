import time
from Classes.Super.Train import Train
from Classes.Functions.Line import getStopListFromLineName
import uuid

class TrainLoader():
    def __init__(self):
        self.name_dict={'line1':('Northern Line: Edgware → Charing Cross → Kennington',
                                    'Northern Line: Kennington → Charing Cross → Edgware','black'),

                        'line2':('Circle Line: Edgware Road → Hammersmith',
                                    'Circle Line: Hammersmith → Edgware Road','yellow'),

                        'line3':('District Line: Ealing Broadway → Upminster',
                                'District Line: Upminster → Ealing Broadway','green'),

                        'line4':('Jubilee Line: Stratford → Stanmore',
                                'Jubilee Line: Stanmore → Stratford','grey'),

                        'line5':('Metropolitan Line: Aldgate → Amersham',
                                'Metropolitan Line: Amersham → Aldgate','purple'),

                        'line6':('Piccadilly Line: Heathrow Terminal 5 → Cockfosters',
                                'Piccadilly Line: Cockfosters → Heathrow Terminal 5','blue'),

                        'line7':('Victoria Line: Brixton → Walthamstow Central',
                                'Victoria Line: Walthamstow Central → Brixton','aqua'),

                        'line8':
                                ('Bakerloo: Harrow → Elephant',
                                'Bakerloo: Elephant → Harrow','maroon'),
                        'line9':
                                ('Hammersmith & City: Barking → Hammersmith',
                                'Hammersmith & City: Hammersmith → Barking','pink'),
                        'line10':
                                ('Central Line: Woodford → Hainault',
                                'Central Line: Hainault → Woodford','red'),
                        'line11':
                                ('Central Line: White City → Hainault',
                                'Central Line: Hainault → White City','red'),
                        'line12':
                                ('Central Line: Hainault → Ealing Broadway',
                                'Central Line: Ealing Broadway → Hainault','red'),
                        'line13':
                                ('Central Line: West Ruislip → Epping',
                                'Central Line: Epping → West Ruislip','red'),
                        'line14':
                                ('Victoria Line: Seven Sisters → Brixton',
                                'Victoria Line: Brixton → Seven Sisters','turquoise'),
                        'line15':
                                ('Metropolitan Line: Chesham → Aldgate',
                                'Metropolitan Line: Aldgate → Chesham','purple'),
                        'line16':
                                ('Metropolitan Line: Uxbridge → Aldgate',
                                 'Metropolitan Line: Aldgate → Uxbridge','purple'),
                        'line17':
                                ('Metropolitan Line: Watford → Baker Street',
                                'Metropolitan Line: Baker Street → Watford','purple'),
                        'line18':
                                ('District Line: Wimbledon → Edgware Road',
                                'District Line: Edgware Road → Wimbledon','green'),
                        'line19':
                                ('District Line: High Street Kensington → Kensington (Olympia)',
                                'District Line: Kensington (Olympia) → High Street Kensington','green'),
                        'line20':
                                ('District Line: Upminster → Richmond',
                                'District Line: Richmond → Upminster','green'),
                        'line21':
                                ('Northern Line: Morden → Bank → Edgware',
                                'Northern Line: Edgware → Bank → Morden','black'),

                        'line23':
                                ('Northern Line: Morden → Bank → High Barnet',
                                'Northern Line: High Barnet → Bank → Morden','black'),
                        'line24':
                                ('Northern Line: Kennington → Charing Cross → Edgware',
                                'Northern Line: Edgware → Charing Cross → Kennington','black'),
                        'line25':
                                ('Northern Line: High Barnet → Charing Cross → Kennington',
                                'Northern Line: Kennington → Charing Cross → High Barnet','black'),
                        'line26':
                                ('Piccadilly Line: Heathrow Terminal 4 → Cockfosters',
                                'Piccadilly Line: Cockfosters → Heathrow Terminal 4','blue'),
                        'line27':
                                ('Piccadilly Line: Cockfosters → Uxbridge',
                                'Piccadilly Line: Uxbridge → Cockfosters','blue'),
                        'line28':
                            ('Waterloo & City: Bank → Waterloo',
                             'Waterloo & City: Waterloo → Bank','red')
                        }

        self.currentTime=time.time()
        self.finished=False

        self.delay=120


    def load(self,train_dict,spriteDictionary,relation_dict,line_dict,way_dict,node_dict,nodeTraffic_dict,simulation_speed):
        if self.delay!=0:
            if self.delay<0:
                self.delay=0
            if self.delay>0:
                self.delay-=(time.time()-self.currentTime)*simulation_speed

        elif not self.finished and self.delay==0:
            self.delay = 120
            pop_dict={}
            for name in self.name_dict:
                #if current last stop has a train, pop the line from the dictionary
                info=self.name_dict[name]
                color=info[2]
                stops=getStopListFromLineName(relation_dict,way_dict,info[1])
                finalStopId=stops[len(stops)-1]
                if len(nodeTraffic_dict[finalStopId]) >0:
                    pop_dict.update({name:name})
                else:
                    testLine1 = info[0]
                    testLine2 = info[1]
                    train = Train(13, 1.7, testLine1, testLine2, relation_dict, line_dict, way_dict, node_dict, 0, 100, '',
                                  spriteDictionary, 0.01,uuid.uuid4(), 1, 1, 1, 1, 1, 1,color)
                    train_dict.update({train.idObject: train})
                    train_dict.update({train.idObject: train})


            for name in pop_dict:
                if name in self.name_dict:
                    self.name_dict.pop(name)
            if len(train_dict) > 400: #stop loading trains after 600, (that's enough)
                self.finished = True
        self.currentTime = time.time()
