# -*- coding: utf-8 -*-
'''
Created on July 9, 2009

@summary: A Plex Media Server plugin that integrates movies from teteaclaques.tv.
@version: 0.1
@author: Oncleben31
'''

# Import the parts of the Plex Media Server Plugin API we need
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
import lxml, re, sys, locale

# Plugin parameters
PLUGIN_TITLE						= "Têtes à Claques.TV"					# The plugin Title
PLUGIN_PREFIX   					= "/video/TAC.TV"				# The plugin's contextual path within Plex
PLUGIN_HTTP_CACHE_INTERVAL			= 0

# Plugin Icons
PLUGIN_ICON_DEFAULT					= "icon-default.png"

# Plugin Artwork
PLUGIN_ARTWORK						= "art-default.jpg"

#Some URLs for the script
PLUGIN_URL	= "http://www.tetesaclaques.tv/ajax/populerSliderIndex.php"



####################################################################################################

def Start():
	reload(sys)
	sys.setdefaultencoding("utf-8")
	
	# Register our plugins request handler
	Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE.decode('utf-8'), PLUGIN_ICON_DEFAULT, PLUGIN_ARTWORK)
	
	# Add in the views our plugin will support
	
	Plugin.AddViewGroup("Menu", viewMode="InfoList", mediaType="items")
	
	# Set up our plugin's container
	
	#MediaContainer.title1 = PLUGIN_TITLE
	MediaContainer.title1 = PLUGIN_TITLE.decode('utf-8')
	MediaContainer.viewGroup = "Menu"
	MediaContainer.art = R(PLUGIN_ARTWORK)
	
	# Configure HTTP Cache lifetime
	
#	HTTP.SetCacheTime(PLUGIN_HTTP_CACHE_INTERVAL)

####################################################################################################
# The plugin's main menu. 

def MainMenu():
	dir = MediaContainer(art = R(PLUGIN_ARTWORK), viewGroup = "Menu")
	dir.Append(Function(DirectoryItem(CollectionDate, title=L("Classement par date"), summary=L("Tous les épisodes par ordre de sortie du plus récent au plus ancien."))))
	dir.Append(Function(DirectoryItem(CollectionVote, title=L("Classement par vote"), summary=L("Tous les épisodes par ordre de préférence des visiteurs"))))
		 
	return dir

####################################################################################################
def CollectionDate(sender):
	dir = RecupererListe("date")
	return dir

def CollectionVote(sender):
	dir = RecupererListe("vote")
	return dir

def RecupererListe(classification) :
	dir = MediaContainer(art = R(PLUGIN_ARTWORK), viewGroup = "Menu", title2 = L("Liste des video"))
	compteurVideo = 15
	section = 0
	
	while compteurVideo == 15 :
		compteurVideo = 0
		
		urldonneesHTML = PLUGIN_URL + "?serie=null&vid=null&vidToSlide="+ str(section*15) +"&playOverlay=null&classification=" + classification + "&selection=collection"
		donneesHTML = XML.ElementFromURL(urldonneesHTML, isHTML=True, encoding="utf-8")
		#Log("donneesHTML %s" % (lxml.etree.tostring(donneesHTML)))
	
		for c in donneesHTML.xpath("//div[@class='size']"):
			id = c.find("span").get("id")
			Log("id %s" % (id))
			
			# Condition de detection de fin
			if id is None:
				break
			
			nom = c.find("span").text.encode("iso-8859-1").decode("utf-8")
			Log("nom %s" % (nom))
			
			thumbAndMore = c.find("img").get("style")
			thumb = thumbAndMore.rsplit("url(")[1].split(")")[0]
			
			# Patch pour bugs dans l'adresse des images
			Log("DEBUG thumb %s" % (thumb[0:5]))
			if thumb[0:6] == "images" :
				urlImage = thumb.split("vignette/")[1]
				thumb = "http://image.tetesaclaques.tv/videos/"+urlImage
				
			Log("thumb %s" % (thumb))
			
			urlVideo = "http://video.tetesaclaques.tv/videos/" + thumb.split("/videos/")[1].rsplit(".jpg")[0] + ".flv"
			Log("urlVideo %s" % (urlVideo))
			
			dir.Append(VideoItem(urlVideo, title=nom, thumb=thumb)) 
			compteurVideo = compteurVideo + 1
			
		section = section + 1
		Log("###### nombre de video : %s" % compteurVideo)
		Log("###### section : %s" % section)
		
	return dir







