# PROGRAMA PARA APLICAÇÃO DO AP1
import serial
import math
import time
import struct
from time import localtime, strftime

# Configura a serial
# para COM# o número que se coloca é n-1 no primeiro parâmetrso. Ex COM9  valor 8
n_serial = raw_input("Digite o número da serial = ") #seta a serial
#n_serial1 = int(n_serial) - 1
ser = serial.Serial("com"+n_serial, 9600, timeout=0.5,parity=serial.PARITY_NONE) # seta valores da serial

# Identificação da base
ID_base = raw_input('ID_base = ')

#tempo_amostra = raw_input('Tempo entre amostras = ')

# Cria o vetor Pacote
Pacote = {}



# Cria Pacote de 52 bytes com valor zero em todas as posições
for i in range(0,52): # faz um array com 52 bytes
   Pacote[i] = 0

while True:
   try:

      contador_tot = 0
      contador_pot = 0
      potmediad = 0.0
      potacumulad = 0.0
      potmeddbd = 0.0
      contador_err = 0

      potmediau = 0.0
      potacumulau = 0.0
      potmeddbu = 0.0
      PER = 0


      # Imprime na tela o menu de opções
      print 'Escolha um comandos abaixos e depois enter'
      print '1 - Realiza medidas:'
      print 's - Para sair:'

      Opcao = raw_input('Entre com a Opção = ')

      # Limpa o buffer da serial
      ser.flushInput()

      # Coloca no pacote o ID_base
      
      Pacote[10] = int(ID_base)
      Pacote[37] = 1    #Liga o LDR

      # Leitura de temperatura e luminosidade
      if Opcao == "1":
         ID_sensor = raw_input('ID_sensor = ')      # Identificação do sensor a ser acessado
         Pacote[8] = int(ID_sensor) # Coloca no pacote o ID_sensor
         num_medidas = raw_input('Entre com o número de medidas = ')
         w = int(num_medidas)

         filename1 = strftime("Sensor_%Y_%m_%d_%H-%M-%S.txt")
         print "Arquivo de log: %s" % filename1
         S = open(filename1, 'w')
         
         for j in range(0,w):
            for k in range(0,52): # transmite pacote
               TXbyte = chr(Pacote[k])
               ser.write(TXbyte)
            # Aguarda a resposta do sensor
            time.sleep(0.3)

            line = ser.read(52) # faz a leitura de 52 bytes do buffer que recebe da serial pela COM
            if len(line) == 52:

               rssid = ord(line[0]) # RSSI_DownLink
               rssiu = ord(line[2]) # RSSI_UpLink
         
               #RSSI Downlink
               if rssid > 128:
                  RSSId=((rssid-256)/2.0)-74
            
               else:
                  RSSId=(rssid/2.0)-74

               #RSSI Uplink
               if rssiu > 128:
                  RSSIu=((rssiu-256)/2.0)-74
            
               else:
                  RSSIu=(rssiu/2.0)-74

               count = ord(line[12])      # contador de pacotes enviados pelo sensor

               # Leitura do AD0
               ad0t = ord(line[16]) # tipo de sensor - no caso está medindo temperatura 
               ad0h = ord(line[17]) # alto
               ad0l = ord(line[18]) # baixo
               AD0 = (ad0h * 256 + ad0l)/100.0
            
               
               contador_pot=contador_pot+1
               potmwd = pow(10,(RSSId/10))
               potacumulad = potacumulad + potmwd

               potmwu = pow(10,(RSSIu/10))
               potacumulau= potacumulau + potmwu

               print'Número do pacote = ',count, 'RSSI DownLink = ', RSSId, '  RSSI UpLink ', RSSIu          
               #print >>S,time.asctime(),' Número do pacote = ',count, 'RSSI DownLink = ', RSSId, '  RSSI UpLink ', RSSIu, ' Temp = ', AD0
               
               
            else:
               contador_err = contador_err + 1
               print ' erro'
               print >>S,time.asctime(),' erro'
               ser.flushInput()
               time.sleep(0.5)

            contador_tot = contador_tot + 1
            #time.sleep(1)

         potmediad = potacumulad /contador_pot
         potmeddbd = 10*math.log10(potmediad)
         #print ' A Potência média de downlink foi:', potmediad , ' mW'
         print 'A Potência média de Downlink em dBm foi:', potmeddbd,' dBm'
         print >>S,time.asctime(),' A Potência média de Downlink em dBm foi:', potmeddbd,' dBm'


         potmediau = potacumulau /contador_pot
         potmeddbu = 10*math.log10(potmediau)
         #print ' A Potência média de Uplink foi:', potmediau , ' mW'
         print 'A Potência média de Uplink em dBm foi:', potmeddbu,' dBm'
         print >>S,time.asctime(),' A Potência média de Uplink em dBm foi:', potmeddbu,' dBm'

         PER = float(contador_err)/float(contador_tot)
         print 'A PER foi de:', float(PER),'%'
         print >>S,time.asctime(),'A PER foi de:', float(PER),'%'
         
         S.close()

      if Opcao == "s" or Opcao == "S":# caso o caracter digitado for s          
         ser.close() # fecha a porta COM
         print 'Fim da Execução'  # escreve na tela
         break
            
   except KeyboardInterrupt:
       S.close()
       ser.close()

       break

