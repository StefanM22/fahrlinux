# -*- coding: UTF-8 -*-
"""
Script zum auslesen der Fahrerkarte von DigitalenTachographen


Copyright 2009 Stefan Manteuffel linux@sm-recycling.de

pyscard wir benötigt http://sourceforge.net/projects/pyscard/

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""




import wx

from smartcard.wx.APDUHexValidator import APDUHexValidator
from smartcard.wx.SimpleSCardAppEventObserver import SimpleSCardAppEventObserver

from smartcard.CardConnection import CardConnection
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.System import readers
from sys import stdin, exc_info
from time import *
import binascii 
import array
from datetime import *

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *

from smartcard.CardRequest import CardRequest
from smartcard.CardType import ATRCardType
from struct import *
import os

""" Option zum Debuggen 
define DEBUG 1 einschalten
define DEBUG 0 ausschalten.
Die Ausgabe erfolgt in der Konsole
"""


DEBUG  = 0








[
ID_TEXT_COMMAND,
ID_TEXTCTRL_COMMAND,
ID_TEXT_RESPONSE,
ID_TEXTCTRL_RESPONSE,
ID_TEXT_SW,
ID_TEXT_SW1,
ID_TEXTCTRL_SW1,
ID_TEXT_SW2,
ID_TEXTCTRL_SW2,
ID_CARDSTATE,
ID_TRANSMIT
] = map( lambda x: wx.NewId(), range(11) )

#ID_ABOUT = 101
#ID_EXIT  = 110
#ID_OPEN  = 111

lesen = {}
lesen[1] = [0x00, 0xb0, 0x00, 0x00, 0xc8]
lesen[2] = [0x00, 0xb0, 0x00, 0xc8, 0xc8]
lesen[3] = [0x00, 0xb0, 0x01, 0x90, 0xc8]
lesen[4] = [0x00, 0xb0, 0x02, 0x58, 0xc8]
lesen[5] = [0x00, 0xb0, 0x03, 0x20, 0xc8]
lesen[6] = [0x00, 0xb0, 0x03, 0xe8, 0xc8]
lesen[7] = [0x00, 0xb0, 0x04, 0xb0, 0xc8]
lesen[8] = [0x00, 0xb0, 0x05, 0x78, 0xc8]
lesen[9] = [0x00, 0xb0, 0x06, 0x40, 0xc8]
lesen[10] = [0x00, 0xb0, 0x07, 0x08, 0xc8]
lesen[11] = [0x00, 0xb0, 0x07, 0xd0, 0xc8]
lesen[12] = [0x00, 0xb0, 0x08, 0x98, 0xc8]
lesen[13] = [0x00, 0xb0, 0x09, 0x60, 0xc8]
lesen[14] = [0x00, 0xb0, 0x0a, 0x28, 0xc8]
lesen[15] = [0x00, 0xb0, 0x0a, 0xf0, 0xc8]
lesen[16] = [0x00, 0xb0, 0x0b, 0xb8, 0xc8]
lesen[17] = [0x00, 0xb0, 0x0c, 0x80, 0xc8]
lesen[18] = [0x00, 0xb0, 0x0d, 0x48, 0xc8]
lesen[19] = [0x00, 0xb0, 0x0e, 0x10, 0xc8]
lesen[20] = [0x00, 0xb0, 0x0e, 0xd8, 0xc8]
lesen[21] = [0x00, 0xb0, 0x0f, 0xa0, 0xc8]
lesen[22] = [0x00, 0xb0, 0x10, 0x68, 0xc8]
lesen[23] = [0x00, 0xb0, 0x11, 0x30, 0xc8]
lesen[24] = [0x00, 0xb0, 0x11, 0xf8, 0xc8]
lesen[25] = [0x00, 0xb0, 0x12, 0xc0, 0xc8]
lesen[26] = [0x00, 0xb0, 0x13, 0x88, 0xc8]
lesen[27] = [0x00, 0xb0, 0x14, 0x50, 0xc8]
lesen[28] = [0x00, 0xb0, 0x15, 0x18, 0xc8]
lesen[29] = [0x00, 0xb0, 0x15, 0xe0, 0xc8]
lesen[30] = [0x00, 0xb0, 0x16, 0xa8, 0xc8]
lesen[31] = [0x00, 0xb0, 0x17, 0x70, 0xc8]
lesen[32] = [0x00, 0xb0, 0x18, 0x38, 0xc8]
lesen[33] = [0x00, 0xb0, 0x19, 0x00, 0xc8]
lesen[34] = [0x00, 0xb0, 0x19, 0xc8, 0xc8]
lesen[35] = [0x00, 0xb0, 0x1a, 0x90, 0xc8]
lesen[36] = [0x00, 0xb0, 0x1b, 0x58, 0xc8]
lesen[37] = [0x00, 0xb0, 0x1c, 0x20, 0xc8]
lesen[38] = [0x00, 0xb0, 0x1c, 0xe8, 0xc8]
lesen[39] = [0x00, 0xb0, 0x1d, 0xb0, 0xc8]
lesen[40] = [0x00, 0xb0, 0x1e, 0x78, 0xc8]
lesen[41] = [0x00, 0xb0, 0x1f, 0x40, 0xc8]
lesen[42] = [0x00, 0xb0, 0x20, 0x08, 0xc8]
lesen[43] = [0x00, 0xb0, 0x20, 0xd0, 0xc8]
lesen[44] = [0x00, 0xb0, 0x21, 0x98, 0xc8]
lesen[45] = [0x00, 0xb0, 0x22, 0x60, 0xc8]
lesen[46] = [0x00, 0xb0, 0x23, 0x28, 0xc8]
lesen[47] = [0x00, 0xb0, 0x23, 0xf0, 0xc8]
lesen[48] = [0x00, 0xb0, 0x24, 0xb8, 0xc8]
lesen[49] = [0x00, 0xb0, 0x25, 0x80, 0xc8]
lesen[50] = [0x00, 0xb0, 0x26, 0x48, 0xc8]
lesen[51] = [0x00, 0xb0, 0x27, 0x10, 0xc8]
lesen[52] = [0x00, 0xb0, 0x27, 0xd8, 0xc8]
lesen[53] = [0x00, 0xb0, 0x28, 0xa0, 0xc8]
lesen[54] = [0x00, 0xb0, 0x29, 0x68, 0xc8]
lesen[55] = [0x00, 0xb0, 0x2a, 0x30, 0xc8]
lesen[56] = [0x00, 0xb0, 0x2a, 0xf8, 0xc8]
lesen[57] = [0x00, 0xb0, 0x2b, 0xc0, 0xc8]
lesen[58] = [0x00, 0xb0, 0x2c, 0x88, 0xc8]
lesen[59] = [0x00, 0xb0, 0x2d, 0x50, 0xc8]
lesen[60] = [0x00, 0xb0, 0x2e, 0x18, 0xc8]
lesen[61] = [0x00, 0xb0, 0x2e, 0xe0, 0xc8]
lesen[62] = [0x00, 0xb0, 0x2f, 0xa8, 0xc8]
lesen[63] = [0x00, 0xb0, 0x30, 0x70, 0x5c]
#readdatum = ""
   
#test = 0


class Fahrlinx( wx.Panel, SimpleSCardAppEventObserver ):
    '''A simple panel that displays activated cards and readers and can
    send APDU to a connected card.'''


    def __init__( self, parent ):
        wx.Panel.__init__( self, parent, -1 )
        SimpleSCardAppEventObserver.__init__( self )
        self.layoutControls()



        self.Bind( wx.EVT_BUTTON, self.OnTransmit, self.transmitbutton)



    def OnActivateCard( self, card ):
        """Called when a card is activated by double-clicking on the card or reader tree control or toolbar.
        In this sample, we just connect to the card on the first activation."""
        SimpleSCardAppEventObserver.OnActivateCard( self, card )
	datumlesen( self )
	if DEBUG == 1:
		print "test debug", self.readdatum
	
	ID_TEXTCTRL_RESPONSE=self.readdatum
        self.feedbacktext1.SetLabel( 'Vorname: ' + `self.VorName` )
        self.feedbacktext2.SetLabel( 'Namame : ' + `self.NachName` )
        self.feedbacktext.SetLabel( 'Letztes Lesedatum: ' + `self.readdatum` )
        self.transmitbutton.Enable()
	
    def OnActivateReader( self, reader ):
        """Called when a reader is activated by double-clicking on the reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnActivateReader( self, reader )
        self.feedbacktext.SetLabel( 'Activated reader: ' + `reader` )
        self.transmitbutton.Disable()

    def OnDeactivateCard( self, card ):
        """Called when a card is deactivated in the reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnActivateCard( self, card )
        self.feedbacktext.SetLabel( 'Deactivated card: ' + `card` )
        self.transmitbutton.Disable()

    def OnDeselectCard( self, card ):
        """Called when a card is selected by clicking on the card or reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnSelectCard( self, card )
        self.feedbacktext.SetLabel( 'Deselected card: ' + `card` )
        self.transmitbutton.Disable()

    def OnSelectCard( self, card ):
        """Called when a card is selected by clicking on the card or reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnSelectCard( self, card )

        self.feedbacktext.SetLabel( 'Selected card: '  )
        if hasattr( self.selectedcard, 'connection' ):
            self.transmitbutton.Enable()

	    
    def OnSelectReader( self, reader ):
        """Called when a reader is selected by clicking on the reader tree control or toolbar."""
        SimpleSCardAppEventObserver.OnSelectReader( self, reader )
        self.feedbacktext.SetLabel( 'Selected reader: ' + `reader` )
        self.transmitbutton.Disable()

    # callbacks
    def OnTransmit( self, event ):
        if hasattr( self.selectedcard, 'connection' ):
            kartelesen(self)
	    if DEBUG == 1:
	      print "Lesen fertig "
	    datumsetzen(self)
	    if DEBUG == 1:
	      print "Datum setzen fertig"
        event.Skip()

    def OnAbbruch(self, event):
	    self.GetParent().Destroy()
	    
	    
    def layoutControls( self ):

	self.feedbacktext1 = wx.StaticText( self, ID_CARDSTATE, "", wx.Point(20, 30), wx.Size(140, -1) )
	self.feedbacktext2 = wx.StaticText( self, ID_CARDSTATE, "", wx.Point(500, 600), wx.Size(140, -1) )
	self.feedbacktext = wx.StaticText( self, ID_CARDSTATE, "", wx.DefaultPosition, wx.DefaultSize, 0 )
	
	
	
        # layout controls
        boxsizerCommand = wx.BoxSizer( wx.HORIZONTAL )

        boxsizerResponse = wx.BoxSizer( wx.HORIZONTAL )

        boxsizerSW = wx.BoxSizer( wx.HORIZONTAL )

        item11 = wx.BoxSizer( wx.HORIZONTAL )
        item11.Add( boxsizerSW, 0, wx.EXPAND | wx.ALL, 5 )

        boxsizerResponseAndSW = wx.BoxSizer( wx.VERTICAL )
        boxsizerResponseAndSW.Add( boxsizerResponse, 0, wx.EXPAND|wx.ALL, 5 )
        boxsizerResponseAndSW.Add( item11, 0, wx.EXPAND|wx.ALL, 5 )

        staticboxEvents = wx.StaticBox( self, -1, "" )
        boxsizerEvents = wx.StaticBoxSizer( staticboxEvents, wx.VERTICAL )
        boxsizerEvents.Add( self.feedbacktext1, 0, wx.ALIGN_LEFT | wx.ALL, 5 )
        boxsizerEvents.Add( self.feedbacktext2, 0, wx.ALIGN_LEFT | wx.ALL, 5 )
        boxsizerEvents.Add( self.feedbacktext, 0, wx.ALIGN_LEFT | wx.ALL, 5 )


        sizerboxTransmitButton = wx.BoxSizer( wx.HORIZONTAL )
        sizerboxTransmitButton.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.transmitbutton = wx.Button( self, ID_TRANSMIT, "Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.transmitbutton.Disable()
        sizerboxTransmitButton.Add( self.transmitbutton, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        sizerboxTransmitButton.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        sizerboxstopbutton = wx.BoxSizer( wx.HORIZONTAL )
        sizerboxstopbutton.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.stopbutton = wx.Button( self, ID_TRANSMIT, "Abbruch", wx.Point(200, 211), wx.Size(80, -1))


        sizerPanel = wx.BoxSizer( wx.VERTICAL )
        sizerPanel.Add( boxsizerEvents, 1, wx.EXPAND | wx.ALL, 5 )
        sizerPanel.Add( sizerboxTransmitButton, 1, wx.EXPAND | wx.ALL, 5 )
	
	sizerPanel.Add( sizerboxstopbutton, 1, wx.EXPAND | wx.ALL, 5 )


        self.SetSizer( sizerPanel )
        self.SetAutoLayout(True)
        sizerPanel.Fit(self)




def kartelesen(self):
    def berehash(self):           # nicht speichern
        apdu = [0x80, 0x2a, 0x90, 0x00]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )

            
    # Signatur des hash codes erstellen

    def sighash(self, response):      # an Datei anhängen
        apdu = [0x00, 0x2a, 0x9e, 0x9a, 0x80]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        ss = len(response)
        if DEBUG == 1:
	  print "sighash tag ", tag
        tagneu = [0, 0, 0, 0, 0]
        tagneu[0] = tag[0]
        tagneu[1] = tag[1]
        tagneu[2] = 1
        tagneu[3] = 0
        tagneu[4] = ss
        a = array.array("B", response )
        b = array.array("B", tagneu )
        datei.write(b.tostring())
        datei.write(a.tostring())


    # Auswahl nach Namen für die Kontrollgeräteanwendung

    def kgaw(self):
        apdu = [0x00, 0xa4, 0x04, 0x0c, 0x06, 0xff, 0x54, 0x41, 0x43, 0x48, 0x4f]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )

    def datschreiben(datei, response):
	if DEBUG == 1:
	  print "response 2", response
        a = array.array("B", response )
        b = array.array("B", tag )
        if DEBUG == 1:
	  print "stop 1"
        datei.write(b.tostring())
        datei.write(a.tostring())
        if DEBUG == 1:
	  print "datenschreib fertig"


    def datschreibenoh(datei, response):
        if DEBUG == 1:
	  print "stop 2"
        a = array.array("B", response )
        datei.write(a.tostring())


    if DEBUG == 1:
      print "WB	"
        
    datei = open("file.ddd", "wb")


    # ICC
    if DEBUG == 1:
      print "datei", datei
            #EF = ""
    tag = [0x00, 0x02, 0x00, 0x00, 0x19] # + response
    apdu = [0x00, 0xA4, 0x02, 0x0C, 0x02, 0x00, 0x02]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    apdu = [ 0x00, 0xb0, 0x00, 0x00, 0x19]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    datschreiben(datei, response)
    if sw1 == 144 and sw2 == 0:

    # IC
        tag = [0x00, 0x05, 0x00, 0x00, 0x08] # + response
        apdu = [0x00, 0xA4, 0x02, 0x0C, 0x02, 0x00, 0x05]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        ic = response

        apdu = [ 0x00, 0xb0, 0x00, 0x00, 0x08]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreiben(datei, response)
    if sw1 == 144 and sw2 == 0:
        kgaw(self)

     ###Aplication ID
        tag = [0x05, 0x01, 0x00, 0x00, 0x0a] # + response
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x01]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:


    # Perform HASH of File       Hash für File berechnen
        berehash(self)
    if sw1 == 144 and sw2 == 0:

    # Datei lesen
        apdu = [0x00, 0xb0, 0x00, 0x00, 0x0a ]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreiben(datei, response)
    if sw1 == 144 and sw2 == 0:
            
    # Signatur des hash codes erstellen
        
        sighash(self, response)
      
       # datei auswählen 						Identification
        tag = [0x05, 0x20, 0x00, 0x00, 0x8f] # + response
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x20]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:
        # Hash berechnen
        berehash(self)
    # Datei lesen
        apdu = [ 0x00, 0xb0, 0x00, 0x00, 0x00]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreiben(datei, response)
    if sw1 == 144 and sw2 == 0:
    # Signatur des hash codes erstellen
        sighash(self, response)
        
        kgaw(self)
       
       # datei auswählen 						Events_Data
        tag = [0x05, 0x02, 0x00, 0x06, 0xc0] # + 
	response = ""
        datschreiben(datei, response)
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x02]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:
        # Hash berechnen
        berehash(self)
    # Datei lesen
        i=1
        while i<=8:
            response, sw1, sw2 = self.selectedcard.connection.transmit( lesen[i], CardConnection.T1_protocol )
            if sw1 == 144 and sw2 == 0:
                datschreibenoh(datei, response)
                i = i + 1
            else:
                    i=50
    # Der letzte Block wird nicht aus dem Array gelesen, da er eine andere länge hat
        apdu =[0x00, 0xb0, 0x06, 0x40, 0x80]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreibenoh(datei, response)
    if sw1 == 144 and sw2 == 0:
     
    # Signatur des hash codes erstellen
        sighash(self, response)

#        kgaw(self)

    # datei auswählen 						Faults_Data
        tag = [0x05, 0x03, 0x00, 0x04, 0x80] # + 
	response = ""	
        datschreiben(datei, response)
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x03]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:
        # Hash berechnen
        berehash(self)
    # Datei lesen
        i=1
        while i<=5:
            response, sw1, sw2 = self.selectedcard.connection.transmit( lesen[i], CardConnection.T1_protocol )
            datschreibenoh(datei, response)
            if sw1 == 144 and sw2 == 0:
                i = i + 1
            else:
                i=50
    # Der letzte Block wird nicht aus dem Array gelesen, da er eine andere länge hat
        apdu =[0x00, 0xb0, 0x03, 0xe8, 0x98]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreibenoh(datei, response)
    if sw1 == 144 and sw2 == 0:
    # Signatur des hash codes erstellen
        sighash(self, response)

        kgaw(self)

    # datei auswählen 						Driver_Activity_Data
        tag = [0x05, 0x04, 0x00, 0x30, 0xcc] # + response
	response = ""
        datschreiben(datei, response)
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x04]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:
        # Hash berechnen
        berehash(self)
    # Datei lesen
        i=1
        while i<=62:
            response, sw1, sw2 = self.selectedcard.connection.transmit( lesen[i], CardConnection.T1_protocol )
            datschreibenoh(datei, response)
            if sw1 == 144 and sw2 == 0:
                i = i + 1
            else:
                i=70
    # Der letzte Block wird nicht aus dem Array gelesen, da er eine andere länge hat
        apdu =[0x00, 0xb0, 0x30, 0x70, 0x5c]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreibenoh(datei, response)
    if sw1 == 144 and sw2 == 0:
    # Signatur des hash codes erstellen
        sighash(self, response)
 #       kgaw(self)



    # datei auswählen 						Vehicels_Used
        tag = [0x05, 0x05, 0x00, 0x18, 0x3a] # + 
	response =""
        datschreiben(datei, response)
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x05]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:
        # Hash berechnen
        berehash(self)
    # Datei lesen
    # Lesen als Schleife aus dem Array lesen[]
        i=1
        while i<=31:
            response, sw1, sw2 = self.selectedcard.connection.transmit( lesen[i], CardConnection.T1_protocol )
            datschreibenoh(datei, response)
            if sw1 == 144 and sw2 == 0:
                i = i + 1
            else:
                i=70
    # Der letzte Block wird nicht aus dem Array gelesen, da er eine andere länge hat
        apdu =[0x00, 0xb0, 0x18, 0x38, 0x02]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreibenoh(datei, response)
    if sw1 == 144 and sw2 == 0:
    # Signatur des hash codes erstellen
        sighash(self, response)

        kgaw(self)


    # datei auswählen 						Places
        tag = [0x05, 0x06, 0x00, 0x04, 0x61] # + 
	response = ""
        datschreiben(datei, response)
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x06]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:
        # Hash berechnen
        berehash(self)
    # Datei lesen
    # Lesen als Schleife aus dem Array lesen[]
        i=1
        while i<=5:
            response, sw1, sw2 = self.selectedcard.connection.transmit( lesen[i], CardConnection.T1_protocol )
            datschreibenoh(datei, response)
            if sw1 == 144 and sw2 == 0:
                i = i + 1
            else:
                i=70
    # Der letzte Block wird nicht aus dem Array gelesen, da er eine andere länge hat
        apdu =[0x00, 0xb0, 0x03, 0xe8, 0x79]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreibenoh(datei, response)
    if sw1 == 144 and sw2 == 0:
    # Signatur des hash codes erstellen
        sighash(self, response)

        kgaw(self)


    # datei auswählen 						Control_Activity_Data
        tag = [0x05, 0x08, 0x00, 0x00, 0x2e] # + response
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x08]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:
        # Hash berechnen
        berehash(self)
    # Datei lesen
        apdu = [ 0x00, 0xb0, 0x00, 0x00, 0x2e]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreiben(datei, response)
    if sw1 == 144 and sw2 == 0:
    # Signatur des hash codes erstellen
        sighash(self, response)

        kgaw(self)


    # datei auswählen 						Specific_Conditions
        tag = [0x05, 0x22, 0x00, 0x01, 0x18] # + response
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x22]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:
        # Hash berechnen
        berehash(self)
    # Datei lesen
        apdu = [ 0x00, 0xb0, 0x00, 0x00, 0xc8]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreiben(datei, response)
        apdu = [ 0x00, 0xb0, 0x00, 0xc8, 0x50]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        if DEBUG == 1:
	  print "stop 4"
        datschreibenoh(datei, response)
        
    if sw1 == 144 and sw2 == 0:
    # Signatur des hash codes erstellen
        sighash(self, response)
        
    #Card Zertifikat
        tag = [0xc1, 0x00, 0x00, 0x00, 0xc2] # + response
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0xc1, 0x00]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:

    # lesen
        apdu = [ 0x00, 0xb0, 0x00, 0x00, 0xc2]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        datschreiben(datei, response)
    if sw1 == 144 and sw2 == 0:




    ##   CA Zertifikat 
       tag = [0xc1, 0x08, 0x00, 0x00, 0xc2] # + response
       apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0xc1, 0x08]
       response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if sw1 == 144 and sw2 == 0:

    # Datei lesen
       apdu = [0x00, 0xb0, 0x00, 0x00, 0xc2 ]
       response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
       datschreiben(datei, response)
    if sw1 == 144 and sw2 == 0:


    # Dateinamen zusammensetzten    
    #    
    # Identifikation Kartenhalter
        NachName = ""
        apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x20]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        if DEBUG == 1:
	  print "NachName"
    #    VorName
        apdu = [ 0x00, 0xb0, 0x00, 0x66, 0x01]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        NachName = NachName + chr(response[0])
        NachName = NachName + "_"

    #    NachName
        apdu = [ 0x00, 0xb0, 0x00, 0x42, 0x23]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        ss = len(response)
        i = 0
        while i <  ss:
            bb = response[i]
            NachName = NachName + chr(bb)
            i = i + 1
        NachName = NachName + "_"
        if DEBUG == 1:
	  print "Nachname 2"
    #    Kartenummer
        apdu = [ 0x00, 0xb0, 0x00, 0x01, 0x0e]
        response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
        Kartenummer = response
        ss = len(response)
        i = 0
        if DEBUG == 1:
	  print "fehler?"
        while i <  ss:
	    if DEBUG == 1:
	      print "in while"
            bb = response[i]
            NachName = NachName + chr(bb)
            i = i + 1
        dz = (strftime("C_%Y%m%d_%H%M_"))
        fn = "/" + dz + NachName + ".DDD"
        if DEBUG == 1:
	  print "fn", fn
        
        datei.close()
        if DEBUG == 1:
	  print " Alles Erfolgreich"
    else:
	if DEBUG == 1:
	  print ' keine Fahrerkarte'
        datei.close()



    dir = os.getcwd()
    isdir = dir + "/Download"
    if not os.path.isdir(isdir):
      if DEBUG == 1:
	print "dir", dir
      os.mkdir("Download")
      
    altfile = dir + "/file.ddd"
    neufile = isdir + fn
    os.rename( altfile, neufile )


def datumsetzen(self):
    if DEBUG == 1:
      print "Datum setzen "
    apdu = [0x00, 0xa4, 0x04, 0x0c, 0x06, 0xff, 0x54, 0x41, 0x43, 0x48, 0x4f]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if DEBUG == 1:
      print "response ", response, sw1, sw2
# Datei wählen
    apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x0e]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if DEBUG == 1:
      print "response ", response, sw1, sw2

# Datum erzeugen
    rd = int(mktime(gmtime()))
    a = (rd >> 24) & 255
    b = (rd >> 16) & 255
    c = (rd >> 8) & 255
    d = rd & 255



    apdu = [0x00, 0xd6, 0x00, 0x00, 0x04, a,b,c,d]
# Datum Schreiben
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if DEBUG == 1:
      print "response ", response, sw1, sw2

def datumlesen(self): #führt zum fehler beim lesen. Die Karte muss resetet werden ?
# Datei wählen
    apdu = [0x00, 0xa4, 0x04, 0x0c, 0x06, 0xff, 0x54, 0x41, 0x43, 0x48, 0x4f]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )

    apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x0e]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    # Datum lesen

    apdu = [0x00, 0xb0, 0x00, 0x00, 0x04 ]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    ct = int(toHexString(response, PACK), 16)
    rd = gmtime(ct)
    self.readdatum = strftime("%a  %d.%m.%Y   %H Uhr %M ",rd)
    
    self.VorName = ""
    
    apdu = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x05, 0x20]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )

    apdu = [ 0x00, 0xb0, 0x00, 0x66, 0x23]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    ss = len(response)
    i = 0
    while i <  ss:
         bb = chr(response[i])
	 if bb ==  " ":
	    i = 40
         self.VorName = self.VorName + bb
         i = i + 1
    if DEBUG == 1:
      print "name 1 ", self.VorName


    self.NachName = ""
    #    NachName
    apdu = [ 0x00, 0xb0, 0x00, 0x42, 0x23]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    ss = len(response)
    i = 0
    while i <  ss:
          bb = chr(response[i])
          if bb == " ":
	      i = 40
          self.NachName = self.NachName + bb
          i = i + 1
    if DEBUG == 1:
      print " Die Karte wurde zuletzt gelesen ", self.readdatum 
      
      print " Name ", self.NachName, self.VorName

# Karte zurücksetzen
    apdu = [0x00, 0xa4, 0x02, 0x3F, 0x00, 0x05, 0x20]
    response, sw1, sw2 = self.selectedcard.connection.transmit( apdu, CardConnection.T1_protocol )
    if DEBUG == 1:
      print  " response ", response, sw1, sw2

    
#    self.selectedcard.reconnect()
