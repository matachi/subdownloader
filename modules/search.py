from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
#!/usr/bin/env python
# Copyright (c) 2010 SubDownloader Developers - See COPYING - GPLv3

import logging
import urllib.request, urllib.error, urllib.parse
from xml.dom import minidom
import xml.parsers.expat
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

OnlyLink = ''
FilmLink = ''

try:
    from modules import subtitlefile
except ImportError:
    import sys, os
    sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
    from modules import subtitlefile

class Link(object):
    def OneLink(self, OnlyLink):
        global FilmLink
        if OnlyLink == 0:
            return FilmLink
        elif OnlyLink != 0:
            FilmLink = OnlyLink
            return        
    
class Movie(object):
    def __init__(self, movieInfo):
        #movieInfo is a dict 
        self.MovieName = movieInfo['MovieName']
        self.MovieSiteLink = str(movieInfo['MovieID']['Link'])
        self.IMDBLink = str(movieInfo['MovieID']['LinkImdb'])
        self.IMDBId = movieInfo["MovieImdbID"]
        self.IMDBRating = str(movieInfo['MovieImdbRating'])
        self.MovieYear = str(movieInfo['MovieYear'])
        self.MovieId = int(movieInfo['MovieID']['MovieID']) #this ID will be used when calling the 2nd step function to get the Subtitle Details
        self.subtitles = [] #this is a list of Subtitle objects
        try:
            self.totalSubs = int(movieInfo['TotalSubs']) #Sometimes we get the TotalSubs in the 1st step before we get the details of the subtitles
        except KeyError:
            self.totalSubs = self.get_total_subs()
        
    def get_total_subs(self):
        return len(self.subtitles)
        
    def __repr__(self):
        return "<Movie MovieName: %s, MovieSiteLink: %s, IMDBLink: %s, IMDBRating: %s, MovieYear: %s, MovieId: %s, totalSubs: %s, subtitles: %r>"% (self.MovieName, self.MovieSiteLink, self.IMDBLink, self.IMDBRating, self.MovieYear, self.MovieId, self.totalSubs, self.subtitles)
    

class SearchByName(object):
    def __init__(self):
        self.log = logging.getLogger("subdownloader.modules.search")
        
    def search_movie(self, moviename=None, sublanguageid="eng", MovieID_link=None):
        #xml_url = configuration.General.search_url % (sublanguageid, moviename)
        if MovieID_link:
            xml_url = "http://www.opensubtitles.com%s"% MovieID_link
        elif not moviename:
            return None
        else:
            moviename = moviename.replace(" ","%20")
            xml_url = "http://www.opensubtitles.com/en/search2/sublanguageid-%s/moviename-%s/xml"% (sublanguageid, moviename)
            
        try:    
            xml_page = urllib.request.urlopen(xml_url)
        except:
            return(2)
            
        try:
            self.log.debug("Getting data from '%s'"% xml_url)
            search = self.parse_results(xml_page.read())
        except xml.parsers.expat.ExpatError: # this will happen when only one result is found
            self.log.debug("Getting data from '%s/xml'"% xml_page.url)
            xml_page = urllib.request.urlopen("%s/xml"% xml_page.url)
            search = self.parse_results(xml_page.read())
            
        if search:
            self.log.debug("Returning data")
            movies = search
        else:
            self.log.debug("No data found. Trying '%s'"% xml_page.url)
            xml_page = urllib.request.urlopen("%s"% xml_page.url)
            movies = self.subtitle_info(xml_page.read())
            
        return movies
        
    def search_subtitles(self, IDSubtitle_link):
        xml_url = "http://www.opensubtitles.com%s"% IDSubtitle_link
        xml_page = urllib.request.urlopen(xml_url)
        try:
            search = self.subtitle_info(xml_page.read())
        except xml.parsers.expat.ExpatError: # this will happen when only one result is found
            search = self.subtitle_info(urllib.request.urlopen(xml_page.url + "/xml").read())
        return search
        
    def subtitle_info(self, raw_xml):
        dom = minidom.parseString(raw_xml) #Make the dom from raw xml
        entries=dom.getElementsByTagName('opensubtitles') #Pull out all entry's
        subtitle_entries=[] #Make an empty container to fill up and return
        data=None
        for entry in entries:
            if entry.getElementsByTagName('SubBrowse'):
                for result in entry.getElementsByTagName('SubBrowse'):
                    if result.getElementsByTagName('Subtitle'):
                        data = result.getElementsByTagName('Subtitle')
                        break
                break
        #print "data=", data
        if not data:
            return []
        # catch subtitle information
        
        for entry in data:
            sub_obj = subtitlefile.SubtitleFile(online=True)
            sub = {}
            if entry.getElementsByTagName('LinkDetails') and entry.getElementsByTagName('LinkDetails')[0].firstChild:
                sub['LinkDetails'] = entry.getElementsByTagName('LinkDetails')[0].firstChild.data
            if entry.getElementsByTagName('IDSubtitle'):
                sub['IDSubtitle'] = { 'IDSubtitle': entry.getElementsByTagName('IDSubtitle')[0].firstChild.data, 
                                                    'Link': entry.getElementsByTagName('IDSubtitle')[0].getAttribute('Link'), 
                                                }
                sub_obj._onlineId = sub['IDSubtitle']['IDSubtitle']
            if entry.getElementsByTagName('MovieReleaseName') and entry.getElementsByTagName('MovieReleaseName')[0].firstChild:
                sub['MovieReleaseName'] = entry.getElementsByTagName('MovieReleaseName')[0].firstChild.data
            if entry.getElementsByTagName('SubFormat') and entry.getElementsByTagName('SubFormat')[0].firstChild:
                sub['SubFormat'] = entry.getElementsByTagName('SubFormat')[0].firstChild.data
                sub_obj.setExtraInfo('format', sub['SubFormat'])
            if entry.getElementsByTagName('SubSumCD') and entry.getElementsByTagName('SubSumCD')[0].firstChild:
                sub['SubSumCD'] = entry.getElementsByTagName('SubSumCD')[0].firstChild.data
                sub_obj.setExtraInfo('totalCDs', sub['SubSumCD'])
            if entry.getElementsByTagName('SubAuthorComment') and entry.getElementsByTagName('SubAuthorComment')[0].firstChild:
                sub['SubAuthorComment'] = entry.getElementsByTagName('SubAuthorComment')[0].firstChild.data
            if entry.getElementsByTagName('SubAddDate') and entry.getElementsByTagName('SubAddDate')[0].firstChild:
                sub['SubAddDate'] = entry.getElementsByTagName('SubAddDate')[0].firstChild.data
            if entry.getElementsByTagName('SubSumVotes') and entry.getElementsByTagName('SubSumVotes')[0].firstChild:
                sub['SubSumVotes'] = entry.getElementsByTagName('SubSumVotes')[0].firstChild.data
            if entry.getElementsByTagName('SubRating') and entry.getElementsByTagName('SubRating')[0].firstChild:
                sub['SubRating'] = entry.getElementsByTagName('SubRating')[0].firstChild.data
                sub_obj.setRating(sub['SubRating'])
            if entry.getElementsByTagName('SubDownloadsCnt') and entry.getElementsByTagName('SubDownloadsCnt')[0].firstChild:
                sub['SubDownloadsCnt'] = entry.getElementsByTagName('SubDownloadsCnt')[0].firstChild.data
                sub_obj.setExtraInfo('totalDownloads', sub['SubDownloadsCnt'])
            if entry.getElementsByTagName('UserNickName') and entry.getElementsByTagName('UserNickName')[0].firstChild:
                sub['UserNickName'] = entry.getElementsByTagName('UserNickName')[0].firstChild.data
                sub_obj._uploader = sub['UserNickName']
            if entry.getElementsByTagName('LanguageName') and entry.getElementsByTagName('LanguageName')[0].firstChild:
                sub['LanguageName'] = entry.getElementsByTagName('LanguageName')[0].firstChild.data
                sub_obj.setLanguageXX(entry.getElementsByTagName('LanguageName')[0].getAttribute('ISO639'))             
            if entry.getElementsByTagName('SubtitleFile'):
                SubtitleFile = {}
                _SubtitleFile = entry.getElementsByTagName('SubtitleFile')[0]

                _File = _SubtitleFile.getElementsByTagName('File')[0]
                SubtitleFile['File'] = {'ID': _SubtitleFile.getElementsByTagName('File')[0].getAttribute('ID'), 
                                                'SubActualCD': {'SubActualCD':_File.getElementsByTagName('SubActualCD')[0].firstChild.data, 
                                                                        'SubSize': _File.getElementsByTagName('SubActualCD')[0].getAttribute('Link'), 
                                                                        'MD5': _File.getElementsByTagName('SubActualCD')[0].getAttribute('MD5'), 
                                                                        'SubFileName': _File.getElementsByTagName('SubActualCD')[0].getAttribute('SubFileName'), 
                                                                        'DownloadLink': _File.getElementsByTagName('SubActualCD')[0].getAttribute('DownloadLink'),  
                                                                        }
                                                }
                
                SubtitleFile['Download'] = {'Download': _SubtitleFile.getElementsByTagName('Download')[0].firstChild.data, 
                                                        'DownloadLink': _SubtitleFile.getElementsByTagName('Download')[0].getAttribute('LinkDownloadBundle'),  
                                                        }
                sub['SubtitleFile'] = SubtitleFile
                global OnlyLink
                OnlyLink = _SubtitleFile.getElementsByTagName('Download')[0].getAttribute('LinkDownloadBundle')
                OnlyLink = ((OnlyLink.replace('dl', 'www')).replace('org/en', 'com')).replace('subb', 'sub')
            if entry.getElementsByTagName('Movie'):
                _Movie = entry.getElementsByTagName('Movie')[0]
                #sub['MovieName'] = _Movie.getElementsByTagName('MovieName')[0].firstChild.data
                sub['MovieID'] = {'MovieID': _Movie.getElementsByTagName('MovieName')[0].getAttribute('MovieID'),
                                            'Link': _Movie.getElementsByTagName('MovieName')[0].getAttribute('Link'),
                                            }
                for section in _Movie.getElementsByTagName('section'):
                    if section.getAttribute('type') == u"about":
                        for info in section.getElementsByTagName("info"):
                            if info.getElementsByTagName("web_url")[0].firstChild.data == u"http://www.imdb.com":
                                sub['MovieID']['LinkImdb'] = info.getElementsByTagName("link_detail")[0].firstChild.data
                                
            if entry.getElementsByTagName('FullName') and entry.getElementsByTagName('FullName')[0].firstChild:
                sub['FullName'] = entry.getElementsByTagName('FullName')[0].firstChild.data
            if entry.getElementsByTagName('ReportLink') and entry.getElementsByTagName('ReportLink')[0].firstChild:
                sub['ReportLink'] = entry.getElementsByTagName('ReportLink')[0].firstChild.data
            # just s shortcut
            sub['DownloadLink'] = sub['SubtitleFile']['File']['SubActualCD']['DownloadLink']
            Link().OneLink(OnlyLink)
            if sub:
                subtitle_entries.append(sub)
        return (subtitle_entries, sub_obj)
            
    def parse_results(self, raw_xml):
        """Parse the xml and return a list of dictionaries like:
            [   {'IDSubtitle': 'foo', 
                    'LinkUseNext': 'foo', 
                    'MovieName': 'foo_movie',
                    ...
                }, 
                {'IDSubtitle': 'foo', 
                    'LinkUseNext': 'foo', 
                    'MovieName': 'foo_movie',
                    ...
                }, 
                ...]
        """
        

        dom = minidom.parseString(raw_xml) #Make the dom from raw xml
        entries=dom.getElementsByTagName('opensubtitles') #Pull out all entry's
        result_entries=[] #Make an empty container to fill up and return
        data = None
        # fetch the wanted result xml node
        for entry in entries:
            if len(entry.getElementsByTagName('results')) > 0:
                for result in entry.getElementsByTagName('results'):
                    if len(result.getElementsByTagName('subtitle')) > 0:
                        data = result.getElementsByTagName('subtitle')
                        break
                break
        #print "data=", data
        if not data:
            return []
        # catch all subtitles information
        for entry in data:
            try:
                sub_obj = subtitlefile.SubtitleFile(online=True)
                sub = {}
                
                if entry.getElementsByTagName('EpisodeName'):
                    return
                if entry.getElementsByTagName('IDSubtitle'):
                    sub['IDSubtitle'] = { 'IDSubtitle': entry.getElementsByTagName('IDSubtitle')[0].firstChild.data, 
                                                        'Link': entry.getElementsByTagName('IDSubtitle')[0].getAttribute('Link'), 
                                                        'LinkImdb': entry.getElementsByTagName('IDSubtitle')[0].getAttribute('LinkImdb'), 
                                                        'DownloadLink': entry.getElementsByTagName('IDSubtitle')[0].getAttribute('DownloadLink'), 
                                                        'uuid': entry.getElementsByTagName('IDSubtitle')[0].getAttribute('uuid'), 
                                                    }
                    sub_obj._onlineId = sub['IDSubtitle']['IDSubtitle']
                if entry.getElementsByTagName('UserID'):
                    sub['UserID'] = { 'UserID': entry.getElementsByTagName('UserID')[0].firstChild.data, 
                                                'Link': entry.getElementsByTagName('UserID')[0].getAttribute('Link'), 
                                                }
                if entry.getElementsByTagName('UserNickName') and entry.getElementsByTagName('UserNickName')[0].firstChild:
                    sub['UserNickName'] = entry.getElementsByTagName('UserNickName')[0].firstChild.data
                    sub_obj._uploader = sub['UserNickName']
                if entry.getElementsByTagName('MovieID'):
                    #sub['MovieID'] = entry.getElementsByTagName('MovieID')[0].firstChild.data
                    sub['MovieID'] = { 'MovieID': entry.getElementsByTagName('MovieID')[0].firstChild.data, 
                                                        'Link': entry.getElementsByTagName('MovieID')[0].getAttribute('Link'), 
                                                        'LinkImdb': entry.getElementsByTagName('MovieID')[0].getAttribute('LinkImdb'), 
                                                    }
                if entry.getElementsByTagName('MovieThumb') and entry.getElementsByTagName('MovieThumb')[0].firstChild:
                    sub['MovieThumb'] = entry.getElementsByTagName('MovieThumb')[0].firstChild.data
                if entry.getElementsByTagName('LinkUseNext') and entry.getElementsByTagName('LinkUseNext')[0].firstChild:
                    sub['LinkUseNext'] = entry.getElementsByTagName('LinkUseNext')[0].firstChild.data
                if entry.getElementsByTagName('LinkZoozle') and entry.getElementsByTagName('LinkZoozle')[0].firstChild:
                    sub['LinkZoozle'] = entry.getElementsByTagName('LinkZoozle')[0].firstChild.data
                if entry.getElementsByTagName('LinkTorrentbar') and entry.getElementsByTagName('LinkTorrentbar')[0].firstChild:
                    sub['LinkTorrentbar'] = entry.getElementsByTagName('LinkTorrentbar')[0].firstChild.data
                if entry.getElementsByTagName('LinkBoardreader') and entry.getElementsByTagName('LinkBoardreader')[0].firstChild:
                    sub['LinkBoardreader'] = entry.getElementsByTagName('LinkBoardreader')[0].firstChild.data
                if entry.getElementsByTagName('MovieName') and entry.getElementsByTagName('MovieName')[0].firstChild:
                    sub['MovieName'] = entry.getElementsByTagName('MovieName')[0].firstChild.data
                if entry.getElementsByTagName('MovieYear') and entry.getElementsByTagName('MovieYear')[0].firstChild:
                    sub['MovieYear'] = entry.getElementsByTagName('MovieYear')[0].firstChild.data
                if entry.getElementsByTagName('MovieImdbRating') and entry.getElementsByTagName('MovieImdbRating')[0].firstChild:
                    sub['MovieImdbRating'] = entry.getElementsByTagName('MovieImdbRating')[0].firstChild.data
                elif not entry.getElementsByTagName('MovieImdbRating')[0].firstChild:
                    sub['MovieImdbRating'] = 0
                if entry.getElementsByTagName('MovieImdbID') and entry.getElementsByTagName('MovieImdbID')[0].firstChild:
                    sub['MovieImdbID'] = entry.getElementsByTagName('MovieImdbID')[0].firstChild.data
                if entry.getElementsByTagName('SubAuthorComment'):
                    try:
                        sub['SubAuthorComment'] = entry.getElementsByTagName('SubAuthorComment')[0].firstChild.data
                    except AttributeError:
                        sub['SubAuthorComment'] = entry.getElementsByTagName('SubAuthorComment')[0].firstChild
                if entry.getElementsByTagName('ISO639'):
                    sub['ISO639'] = { 'ISO639': entry.getElementsByTagName('ISO639')[0].firstChild.data, 
                                                'LinkSearch': entry.getElementsByTagName('ISO639')[0].getAttribute('LinkSearch'), 
                                                'flag': entry.getElementsByTagName('ISO639')[0].getAttribute('flag'), 
                                                }
                    sub_obj.setLanguageXX(sub['ISO639']['ISO639'])
                    #sub_obj._onlineId = sub['IDSubtitle']['IDSubtitle']
                    #It does require the Subtitle ID to downlad, not the Subtitle File Id
                    sub_obj.setExtraInfo('downloadLink', "http://www.opensubtitles.com/download/sub/%s" % sub_obj.getIdOnline()) 
                if entry.getElementsByTagName('LanguageName') and entry.getElementsByTagName('LanguageName')[0].firstChild:
                    sub['LanguageName'] = entry.getElementsByTagName('LanguageName')[0].firstChild.data
                if entry.getElementsByTagName('SubFormat') and entry.getElementsByTagName('SubFormat')[0].firstChild:
                    sub['SubFormat'] = entry.getElementsByTagName('SubFormat')[0].firstChild.data
                    sub_obj.setExtraInfo('format', sub['SubFormat'])
                if entry.getElementsByTagName('SubSumCD') and entry.getElementsByTagName('SubSumCD')[0].firstChild:
                    sub['SubSumCD'] = entry.getElementsByTagName('SubSumCD')[0].firstChild.data
                    sub_obj.setExtraInfo('totalCDs', sub['SubSumCD'])
                if entry.getElementsByTagName('SubAddDate') and entry.getElementsByTagName('SubAddDate')[0].firstChild:
                    sub['SubAddDate'] = entry.getElementsByTagName('SubAddDate')[0].firstChild.data
                if entry.getElementsByTagName('SubBad') and entry.getElementsByTagName('SubBad')[0].firstChild:
                    sub['SubBad'] = entry.getElementsByTagName('SubBad')[0].firstChild.data
                if entry.getElementsByTagName('SubRating') and entry.getElementsByTagName('SubRating')[0].firstChild:
                    sub['SubRating'] = entry.getElementsByTagName('SubRating')[0].firstChild.data
                    sub_obj.setRating(sub['SubRating'])
                if entry.getElementsByTagName('SubDownloadsCnt') and entry.getElementsByTagName('SubDownloadsCnt')[0].firstChild:
                    sub['SubDownloadsCnt'] = entry.getElementsByTagName('SubDownloadsCnt')[0].firstChild.data
                    sub_obj.setExtraInfo('totalDownloads', sub['SubDownloadsCnt'])
                if entry.getElementsByTagName('SubMovieAka') and entry.getElementsByTagName('SubMovieAka')[0].firstChild:
                    sub['SubMovieAka'] = entry.getElementsByTagName('SubMovieAka')[0].firstChild.data
                if entry.getElementsByTagName('SubDate') and entry.getElementsByTagName('SubDate')[0].firstChild:
                    sub['SubDate'] = entry.getElementsByTagName('SubDate')[0].firstChild.data
                if entry.getElementsByTagName('SubComments') and entry.getElementsByTagName('SubComments')[0].firstChild:
                    sub['SubComments'] = entry.getElementsByTagName('SubComments')[0].firstChild.data
                if entry.getElementsByTagName('TotalSubs') and entry.getElementsByTagName('TotalSubs')[0].firstChild:
                    sub['TotalSubs'] = entry.getElementsByTagName('TotalSubs')[0].firstChild.data
                if entry.getElementsByTagName('Newest') and entry.getElementsByTagName('Newest')[0].firstChild:
                    sub['Newest'] = entry.getElementsByTagName('Newest')[0].firstChild.data
                if sub:
                    #result_entries.append(sub)
                    temp_movie = Movie(sub)
                    movie_exists = False
                    for movie in result_entries:
                        if movie.MovieId == temp_movie.MovieId:
                            movie_exists = True
                            if hasattr(sub_obj, "_extraInfo") and sub_obj._extraInfo:
                                movie.subtitles.append(sub_obj)
#                            already_movie = result_entries.pop(result_entries.index(movie))
#                            temp_movie.subtitles = already_movie.subtitles
                    if not movie_exists:
                        if hasattr(sub_obj, "_extraInfo") and sub_obj._extraInfo:
                            temp_movie.subtitles.append(sub_obj)
                        result_entries.append(temp_movie)
                    
            except IndexError as e:
                pass
        return result_entries

#For testing purposes
if __name__ == "__main__":  
    import pprint
    s = SearchByName()
    res = s.search_movie("anamorph", "por,pob")
    #pprint.pprint(res)
    for movie in res:
        pprint.pprint(movie)
        print(len(movie.subtitles))
