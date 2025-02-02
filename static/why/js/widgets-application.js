
  
  
  



  
    
  
  








  (function () {
    // This is complex as we need to deal with two difficult cases:
    // 1. Determining the script tag when another script has a similar
    //    name (e.g. application.js).
    // 2. Determining the script tag when other script tags are inserted
    //    after ours before our code can run. This can happen when there are
    //    other async scripts on the page.
    var getCurrentScriptTag = function () {
      // Accurately get current script. Only works in a couple of browsers.
      if (document.currentScript) {
        return document.currentScript;
      }

      // Attempt to find script by end of url.
      var scripts = document.getElementsByTagName('script');
      var possibleScripts = [];
      for (var i = 0; i < scripts.length; i++) {
        var script = scripts[i];
        if (/\/application\.js$/.exec(script.src)) {
          possibleScripts.push(script);
        }
      }

      if (possibleScripts.length === 1) {
        return possibleScripts[0];
      }

      // Default to the last script tag.
      return scripts[scripts.length - 1];
    };

    var getBaseUrl = function () {
      var src = getCurrentScriptTag().src;
      if (!src) {
        return '';
      }
      return src.substring(0, src.lastIndexOf('/')).replace(/\/widgets(\/1)?/, "");
    };

    var loadScript = function (src) {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', src, false);
      xhr.send(null);
      var s = document.createElement('script');
      s.type = "text/javascript";
      s.text = xhr.responseText;
      (document.body || document.head).appendChild(s);
    };

    var oldJQuery = function () {
      try {
        var versions = $.fn.jquery.split('.');
        var version = (versions[0] * 10000) + (versions[1] * 100) + (versions[2] * 1);
        return version < 10700;
      } catch (e) {
        return true;
      }
    };

    var init = function () {
      window.KV = window.KV || {};

      if (window.KV.loaded) {
        return;
      }

      var base = getBaseUrl();

      var version = '919';

      base = base.split("/");
      var staticBase = getBaseUrl().split("/");

      base.push(version);

      window.KV.base = base = base.join("/");

      var staticBase = getBaseUrl().split("/");

      if (staticBase.length > 3) {
        staticBase.pop();
      }

      var staticContentCdnBase = "https://cdn.qumucloud.com/origin/public/rbs.qumucloud.com/staticcontent/919/client";

      window.KV.staticBase = /^https?:/.test(staticContentCdnBase) ? staticContentCdnBase : staticBase.join("/") + staticContentCdnBase;

      var locales = {"widget":{"RestrictedMessage":"This presentation is restricted and cannot be played in the 'light' player","small":"small","Adjust Volume":"Adjust Volume","Email":"Email","MuteUnmute":"Mute / Unmute","Pause":"Pause","Download video":"Download video","Copy to clipboard":"Copy to clipboard","Embed":"Embed","Reactions":"Reactions","No items":"No items","Page":"Page {{page}}","Time":"Time","start at":"start at","medium":"medium","Seek slider":"Seek slider","URL":"URL","Playlist":"Smart Search","ConsentPopupError":"Could not open consent window - is your popup blocker enabled?","WaitingForConsent":"Waiting for consent...","SpeechSearchFailed":"Speech search failed.","Search":"Search","This presentation has been removed or does not exist":"This presentation has been removed or does not exist","current size":"current size","Copy URL":"Copy URL","Open Privacy Settings":"Open Privacy Settings","SpeechSearchInvalidCharactersError":"Invalid characters provided for speech search. The search failed.","Copy and paste the embed code below onto your website":"Copy and paste the embed code below onto your website:","large":"large","active":"active","Presentation":"Presentation","SpeechSearchUnableToGetResults":"Unable to get speech search results.  The search is carried out on the remaining criteria.","Play":"Play","ReviewPolicy":"You must review our privacy policy before viewing this content.","Closed captions":"Closed captions","Next":"Next","Embed mode":"Embed mode","SpeechSearchInvalidCharactersInfo":"Invalid characters provided for speech search. The search is carried out on the remaining criteria.","Embed code":"Embed code","Next page":"Next page","Previous":"Previous","Close":"Close","Previous page":"Previous page","Download audio":"Download audio","None":"None","Share":"Share","Consent required":"Consent required"},"common":{"date":{"november":"November","saturday":"Saturday","august":"August","may":"May","february":"February","july":"July","thursday":"Thursday","april":"April","march":"March","sunday":"Sunday","june":"June","min":{"sunday":"Su","saturday":"Sa","tuesday":"Tu","friday":"Fr","thursday":"Th","wednesday":"We","monday":"Mo"},"september":"September","tuesday":"Tuesday","january":"January","december":"December","friday":"Friday","short":{"november":"Nov","saturday":"Sat","august":"Aug","may":"May","february":"Feb","july":"Jul","thursday":"Thu","april":"Apr","march":"Mar","sunday":"Sun","june":"Jun","september":"Sep","tuesday":"Tue","january":"Jan","december":"Dec","friday":"Fri","wednesday":"Wed","october":"Oct","monday":"Mon"},"wednesday":"Wednesday","october":"October","monday":"Monday"},"metadata":{"Owner":"Owner","Published Date":"Published Date","Modified Date":"Modified Date","Created Date":"Created Date","Presentation Type":"Presentation Type","does not contain":"does not contain","is not":"is not","Projection Type":"Projection type","Chapter Title":"Chapter Title","Relevance":"Relevance","less than":"less than","is not in the last":"is not in the last","Package State":"Package State","Podcastable":"Podcastable","is in the last":"is in the last","Broadcast Date":"Broadcast Date","Valid From":"Valid From","greater than":"greater than","less than or equal to":"less than or equal to","GUID":"GUID","Title":"Title","Custom":"Custom","is":"is","is not in the next":"is not in the next","Public":"Public","Publisher":"Publisher","greater than or equal to":"greater than or equal to","Built-in":"Built-in","Downloadable":"Downloadable","Allow Feedback":"Allow Feedback","is not in the range":"is not in the range","contains":"contains","is in the next":"is in the next","Alias":"Alias","Valid Until":"Valid Until","External":"External","is in the range":"is in the range","Audio":"Audio","Allow Questions":"Allow Questions"},"Apply":"Apply","projectionType":{"Mono":"360º","None":"2D"},"Minutes":"{{count}} minute","TrueFalseToYesNo":{"No":"No","Yes":"Yes"},"caption hub":{"Caption Hub":""},"Unknown":"Unknown","apiDefaultColumns":{"Status":"Status","Description":"Description","Modified":"Modified","Views":"Views","Untitled":"Untitled","Templates":"Templates","Duration":"Duration","Queued":"Queued ({{percentage}}%)","Requires Access Token":"Requires Access Token","Created":"Created","Processing":"Processing ({{percentage}}%)","Force Https Playback":"Force Https Playback","Type":"Type","Default template":"Default template","Requires Registration":"Requires Registration","Owner username":"Owner username","Published":"Published","Tags":"Tags","Password":"Password","Publisher username":"Publisher username"},"Open sidebar":"Open sidebar","UnsupportedBrowserTitle":"Unsupported Browser","Display Auto-Captions in":"Display Auto-Captions in {{languageCode}}","advancedSearchForm":{"Unassigned metadata scroll over for more information":"Unassigned metadata; scroll over for more information","MetadataTooltip":"The metadata field is not part of a presentation type, please remove the field from the smart search or add it to a presentation type.","Enter text":"Enter text","Remove":"Remove","Select a field":"Select a field","Presentations that match":"Presentations that match","Select a date":"Select a date","Select tags":"Select tags","Select a date and time":"Select a date and time","Speech Search":"Speech Search","Enter email":"Enter email","Choose any or all":"Choose any or all","all":"all","Enter number":"Enter number","Select one or multiple options":"Select one or multiple options","Select a presentation type":"Select a presentation type","Select an option":"Select an option","any":"any","Select a comparator":"Select a comparator","NoRulesText":"No rules - all presentations will be returned.","Select users":"Select users","Select a state":"Select a state","of the following rules":"of the following rules:","Choose yes or no":"Choose yes or no","to":"to","Enter a range":"Enter a range","Select a bound":"Select a bound"},"UnsupportedBrowserMessage":"Your browser is not supported. Please upgrade to a modern browser listed on the page linked below.","packageState":{"Pending Approval":"Pending Approval","Draft":"Draft","Pending Publication":"Pending Publication","Revision":"Revision","Pending Review":"Pending Review","Hidden":"Hidden","Published":"Published","Withdrawn":"Withdrawn","Deleted":"Deleted","Processing":"Processing"},"typeAheadInput":{"Current User":"Current User","Placeholder":"Enter a {{typeName}}...","types":{"metadata":"metadata name","tag":"tag","user":"user"}},"Display Auto-Captions":"Display Auto-Captions","MANUAL_FAILOVER":"Manual Failover","popover":{"Dismiss":"Dismiss"},"playerActionTrigger":{"On post-roll start":"On post-roll start","On main content start":"On main content start","On advert start":"On advert start","Chapter":"Chapter","Time":"Time","On pre-roll start":"On pre-roll start"},"AudienceReactionsNotForPublishedPresentation":"Audience Reactions cannot be edited after publishing or once the event is over.","playerActionType":{"Replace player with web page":"Replace player with web page...","Show tab":"Show tab...","TimeString":"hh:mm:ss.s","Switch to large video":"Switch to large video","for":"for","Show web page in pop-up window":"Show web page in pop-up window...","Restore player":"Restore player","Skip to time":"Skip to time...","Switch to alternative layout":"Switch to alternative layout","seconds":"seconds","Pause video for":"Pause video for...","Highlight captions button":"Highlight captions button...","Run script":"Run script...","Maximize player":"Maximize player","Switch to large slides":"Switch to large slides","Move PIP box":"Move PIP box to...","Load web page as slide":"Load web page as slide...","Enter JavaScript":"Enter JavaScript","Switch to default layout":"Switch to default layout","Switch to slides only":"Switch to slides only","Pause video":"Pause video","Info":"e.g. info","Highlight embed button":"Highlight embed button...","Play video":"Play video","Highlight feedback button":"Highlight feedback button...","Switch to video only":"Switch to video only","ExampleUrl":"e.g. http://www.qumu.com","Ping URL":"Ping URL..."},"userInterface":{"HijackingMessage":"You are attempting to leave this page. You may lose any unsaved work."},"AUTOMATIC_FAILOVER":"Automatic Failover","unit":{"MonthsShort":"mo","MinutesShort":"m","DaysShort":"d","SecondsShort":"s","HoursShort":"h"},"Next":"Next","closedCaptions":{"Auto":"[auto]","Caption Hub":"[caption hub]","Encoder":"[encoder]"},"header":{"Help":"Help","Preferences":"Preferences","Log out":"Log out"},"playerOverlay":{"Player Overlay":"Player Overlay","NO_WATERMARKS":"No watermark","CREATORS_DISCRETION":"Creator's discretion","FIVE_WATERMARKS":"5 watermarks","THREE_WATERMARKS":"3 watermarks","FOUR_WATERMARKS":"4 watermarks","ONE_WATERMARK":"1 watermark","TWO_WATERMARKS":"2 watermarks"},"appProperties":{"ForbiddenAccessLabelText":"Access Restricted: You were redirected here due to insufficient permissions.","Return to login page":"Return to login page","SyncErrorText":"There was an error synchronizing your changes with the server.\nIt is recommended you save any changes and reload.","SessionTimeoutLabelText":"Your session has timed out."},"metadataType":{"DATE":"Date","NUMBER":"Number","LARGE_TEXT":"Large text","MULTI_SELECT":"Multi select","TEXT":"Text","DATE_TIME":"Date time","EMAIL":"Email","BOOLEAN":"Yes or No","SELECT":"Select","TAGS":"Tags"},"controlPanel":{"TimeOfDuration":"{{time}} of {{duration}}"},"dateError":{"The date should be after":"The date should be after {{startDate}}","The date should be before":"The date should be before {{endDate}}"},"pagination":{"Next Page":"Next Page","Previous Page":"Previous Page","CurrentPageIndicator":"{{firstItem}}-{{lastItem}} of {{total}}"},"widget":{"WaitingForDisclaimer":"Waiting for disclaimer..."},"Cancel":"Cancel","Hours":"{{count}} hour","dateRange":{"Last 30 days":"Last 30 days","FromTo":"From {{from}} to {{to}}","Last 7 days":"Last 7 days","Last 90 days":"Last 90 days","All Time":"All Time"},"footer":{"Copyright":"Copyright © Qumu Corporation. All rights reserved."},"Close sidebar":"Close sidebar","See details":"See details","show":"show","Confirm":"Confirm","Viewing now":"Viewing now","bsDatepicker":{"Today":"Today"},"cookies":{"WaitingMsg":"Waiting for cookies...","Cookies Required":"Cookies Required","CookiesRequiredMsg":"This page requires cookies. Click here to continue."},"Clear":"Clear","AutoCaptionNotForPublishedPresentation":"Caption languages cannot be edited after publishing","ccLanguages":{"en-IE":"English (Ireland)","hi":"Hindi","ps":"Pashto","pt":"Portuguese","fil":"Filipino","hr":"Croatian","hu":"Hungarian","yi":"Yiddish","hy":"Armenian","zh-Hans":"Chinese (Simplified Han)","zh-Hant":"Chinese (Traditional Han)","yo":"Yoruba","ia":"Interlingua","id":"Indonesian","ie":"Interlingue","aa":"Afar","ab":"Abkhazian","ik":"Inupiak","qu":"Quechua","af":"Afrikaans","is":"Icelandic","it":"Italian","am":"Amharic","fr-CA":"French (Canada)","iw":"Hebrew","zh":"Chinese","ar":"Arabic","as":"Assamese","pt-PT":"Portuguese (Portugal)","fr-BE":"French (Belgium)","ja":"Japanese","ay":"Aymara","az":"Azerbaijani","rm":"Romance","zu":"Zulu","rn":"Kirundi","ro":"Romanian","ba":"Bashkir","be":"Byelorussian","ru":"Russian","bg":"Bulgarian","rw":"Kinyarwanda","bh":"Bihari","bi":"Bislama","bn":"Bengali","jv":"Javanese","bo":"Tibetan","sa":"Sanskrit","br":"Breton","de-AT":"German (Austria)","sd":"Sindhi","sg":"Sangro","sh":"Croatian","ka":"Georgian","si":"Singhalese","CUSTOM":"Custom","sk":"Slovak","sl":"Slovenian","sm":"Samoan","sn":"Shona","so":"Somali","ca":"Catalan","sq":"Albanian","sr":"Serbian","kk":"Kazakh","ss":"Siswati","kl":"Greenlandic","st":"Sesotho","km":"Cambodian","su":"Sudanese","kn":"Kannada","sv":"Swedish","ko":"Korean","sw":"Swahili","zh-TW":"Chinese (Taiwan)","ks":"Kashmiri","ku":"Kurdish","co":"Corsican","ta":"Tamil","ky":"Kirghiz","cs":"Czech","te":"Telugu","tg":"Tajik","th":"Thai","la":"Latin","ti":"Tigrinya","cy":"Welsh","tk":"Turkmen","tl":"Tagalog","tn":"Setswana","to":"Tonga","da":"Danish","tr":"Turkish","ts":"Tsonga","tt":"Tatar","de":"German","ln":"Lingala","en-US":"English (United States)","lo":"Laothian","tw":"Twi","lt":"Lithuanian","lv":"Latvian","nl-BE":"Dutch (Belgium)","zh-CN":"Chinese (China)","dz":"Bhutani","uk":"Ukrainian","mg":"Malagasy","mi":"Maori","ur":"Urdu","de-CH":"German (Switzerland)","mk":"Macedonian","ml":"Malayalam","mn":"Mongolian","mo":"Moldavian","mr":"Marathi","uz":"Uzbek","ms":"Malay","el":"Greek","mt":"Maltese","en":"English","eo":"Esperanto","my":"Burmese","es":"Spanish","et":"Estonian","eu":"Basque","na":"Nauru","vi":"Vietnamese","zh-SG":"Chinese (Singapore)","ne":"Nepali","vo":"Volapuk","fa":"Persian","fa-AF":"Persian (Afghanistan)","en-GB":"English (United Kingdom)","nl":"Dutch","no":"Norwegian","en-CA":"English (Canada)","fi":"Finnish","fj":"Fiji","fo":"Faeroese","fr":"French","fy":"Frisian","oc":"Occitan","fr-CH":"French (Switzerland)","wo":"Wolof","ga":"Irish","gd":"Gaelic","om":"Oromo","or":"Oriya","gl":"Galician","zh-HK":"Chinese (Hong Kong)","pt-BR":"Portuguese (Brazil)","gn":"Guarani","es-ES":"Spanish (Spain)","es-MX":"Spanish (Latin America)","gu":"Gujarati","xh":"Xhosa","pa":"Punjabi","ha":"Hausa","pl":"Polish"},"security":{"Password protected":"Password protected","Internal":"Internal","Group restricted":"Group restricted"},"alert":{"Warning":"Warning","Error":"Error","Close":"Close"},"pollState":{"Show Results":"Show Results","Closed":"Closed","Open":"Open"},"defaultPlayerView":{"options":{"MULTI_CLIP":"Multi Clip","PICTURE_IN_PICTURE_LARGE_SLIDES":"Picture in Picture, large slides","SIDE_BY_SIDE":"Side by side","CREATORS_DISCRETION":"Creator's discretion","PICTURE_IN_PICTURE_SMALL_SLIDES":"Picture in Picture, small slides"},"label":"Default Player View","type":{"SINGLE_CLIP":"Single Clip","MULTI_CLIP":"Multi Clip","SOCIALIVE":"Socialive"}},"playerActionTypeOption":{"feedback":"feedback","attachments":"attachments","top-right":"top-right","bottom-right":"bottom-right","chapters":"chapters","bottom-left":"bottom-left","custom":"custom","top-left":"top-left","share":"share","speech search":"speech search","info":"info"},"charting":{"mega":"M","resetZoom":"Reset zoom","decimalPoint":".","downloadPDF":"Download PDF document","downloadJPEG":"Download JPEG image","printChart":"Print chart","giga":"G","loading":"Loading...","resetZoomTitle":"Reset zoom level 1:1","downloadPNG":"Download PNG image","exa":"E","downloadSVG":"Download SVG vector image","kilo":"k","contextButtonTitle":"Chart context menu","peta":"P","tera":"T","drillUpText":"Back to {series.name}","noData":"No data to display","thousandsSep":","},"Hours_plural":"{{count}} hours","value":"value","dateTimeSpan":{"hours":"hours","months":"months","weeks":"weeks","minutes":"minutes","days":"days","years":"years"},"disclaimer":{"Open Disclaimer Window":"Open Disclaimer Window","Agree and View Presentation":"Agree &amp; View Presentation","Disclaimer Required":"Disclaimer Required","AcceptDisclaimerMsg":"This presentation requires you to accept a disclaimer.","Continue":"Continue","Seconds before the presentation start":"Seconds before the presentation starts:","PleaseAccept":"Please accept the disclaimer in order to proceed."},"key":"key","Captions from encoder":"Captions from encoder","PleaseSelect":"-- Please select --","os":{"MacOS":"MacOS","Windows":"Windows"},"privacySettings":{"PopupErrorMessage":"Could not open privacy settings popup - is your popup blocker enabled?"},"audienceReactions":{"1F601":"Laugh","1F44F":"Clap","Available Reactions":"Available Reactions","1F44E":"Dislike","2764":"Love","1F62E":"Surprised","Live Audience Reactions":"Live Audience Reactions","Selected Reactions":"Selected Reactions","1F389":"Party","1F44D":"Like","Default Reactions":"Default Reactions"},"hide":"hide","BroadcastOn":"Scheduled for {{datetime}}","form":{"NameIsRequired":"$t({{name}}) is required","NameIsHexadecimalColor":"$t({{name}}) has to be a valid hexadecimal color","NameIsTooLong":"$t({{name}}) can't be longer than $t({{max}}) characters"},"AutoCaptionNotForLiveEventWithEncoderCaptions":"Auto-captions and translations not applicable for live event with captions from encoder","Minutes_plural":"{{count}} minutes","timeFormat":"g:ia","Previous":"Previous","Submit":"Submit","Seconds":"{{count}} second","Seconds_plural":"{{count}} seconds","Add Auto-Captions Translation Languages":"Add Auto-Captions Translation Languages"}};

      // DEV-6660 add new locales to the existing ones rather than overriding them all
      if (window.KV.locales) {
        for (var name in locales) window.KV.locales[name] = locales[name];
      } else {
        window.KV.locales = locales;
      }

      window.KV.platformConfig = window.KV.platformConfig || {};

      

      window.KV.platformConfig.consent = {
        isEnabled: false,
        hasConsented: false,
      };

      if (typeof $ === 'undefined' || !$.fn || !$.fn.jquery || oldJQuery()) {
        loadScript(window.KV.staticBase + '/js-lib/widgets/jquery.min.js');
        window.KV.noConflict = true;
      }
      loadScript(window.KV.staticBase + '/application/widgets.js');
    };

    init();

  })();
