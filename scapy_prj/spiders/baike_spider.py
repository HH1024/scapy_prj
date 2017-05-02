# -*- coding:utf-8 -*-

import scrapy
import re, time
import random
import zlib
import bson.binary
from datetime import datetime

from pymongo import MongoClient
connection=MongoClient('localhost',27017) 

#选择myblog库  
db=connection.scapy_baike  

# 使用users集合  
urls_collection=db.urls
content_page_collection=db.content_page

__READY_FOR_SPIDER__ = []
__URL_PREFIX__ = 'https://baike.baidu.com'
__URL_PREFIX_LEN__ = len(__URL_PREFIX__) + 3
__BAIKE_DOMAIN__ = 'baike.baidu.com'
file_suffix = [
    '.css',
    '.js',
    '.svg',
    '.png',
    '.jpg'
]

class BaikeSpider(scrapy.Spider):
    name = "baike"

    def start_requests(self):
        urls = [
            # 'https://baike.baidu.com/',
            r'https://baike.baidu.com/tashuo/browse/content?id=f78312c88b49b6e8f9fbf95f'
        ]
        data = urls_collection.find_one({'used': False})
        if data:
            self.log("first url %s" % data['url'])
            urls_collection.update(
                data,
                {'used': True, 'updated_at': datetime.now(),'url':data['url'], 'created_at': data['created_at']},
                upsert = False
            )
            yield scrapy.Request(url=data['url'] , callback=self.parse)
        else:
            self.log("first url %s" % ('https://baike.baidu.com/'))
            urls_collection.insert({
                'url': 'https://baike.baidu.com/',
                'used': True,
                'created_at': datetime.now()
            })
            yield scrapy.Request(url='https://baike.baidu.com/' , callback=self.parse)
        while 1:
            sleep_time = 8 + random.random() * 10
            data = urls_collection.find_one({'used': False})
            self.log("get next: %s" % data)
            if data:
                self.log("after %s next url %s" % (sleep_time, data['url']))
                time.sleep(sleep_time)
                urls_collection.update(
                    data,
                    {'used': True, 'updated_at': datetime.now(),'url':data['url'], 'created_at': data['created_at']},
                    upsert = False
                )
                yield scrapy.Request(url=data['url'] , callback=self.parse)
            else:
                self.log("after %s next url %s" % (sleep_time, data))
                break
                # time.sleep(sleep_time)
        # for url in urls:
        #     yield scrapy.Request(url=url , callback=self.parse)

    def parse(self, response):
        self.log("body size %s, url:%s" % (len(response.body), response.url))
        data = content_page_collection.find({'url': response.url})
        if not data or data.count() == 0:
            z_body = zlib.compress(response.body)
            self.log("compress %s" % len(z_body))
            content_page_collection.insert({
                'url': response.url,
                'page_content': bson.binary.Binary(z_body),
                'created_at': datetime.now()
            })
        else:
            self.log("repeat scrapy %s" % response.url)
            return
        urls=re.findall(r'<a.*?href=.*?<\/a>', response.body, re.I|re.S|re.M)
        res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
        link_list = []
        for a_url in urls:
            link_list.extend(re.findall(res_url, a_url))
        # self.log(link_list)
        for url in link_list:
            if '#' in url:
                continue
            is_continue = False
            for suffix in file_suffix:
                if suffix in url:
                    is_continue = True
                    break
            if is_continue:
                continue
            if url[0] == '/':
                # self.log("INNNN %s" % url)
                self.__addOneChildUrl__(__URL_PREFIX__+url)
                continue
            if __BAIKE_DOMAIN__ in url[:__URL_PREFIX_LEN__]:
                # self.log("INNNN %s" % url)
                self.__addOneChildUrl__(url)
            # else:
            #     self.log("%s not in %s" % (__BAIKE_DOMAIN__, url))
            # self.log("cannot --- %s" % url)
            # self.log(type(url))
        # self.log('Saved file %s' % filename)

    def __addOneChildUrl__(self, url):
        data = urls_collection.find({'url': url})
        if not data or data.count() == 0:
            # self.log("add url:%s" % url)
            urls_collection.insert({
                'url': url,
                'used': False,
                'created_at': datetime.now()
            })

        # global __READY_FOR_SPIDER__
        # __READY_FOR_SPIDER__.append(url)
        # if len(__READY_FOR_SPIDER__) >= 10:
        #     self.__saveUrlToDB__(__READY_FOR_SPIDER__)
        # __READY_FOR_SPIDER__ = []


# file_suffix = [
#     ".aca"
# ".acf",".acm",".aif",".aifc",".aiff",".ani",".ans",".arc",".arj",".asf",".asp",".asx",".au",".avi",".bak"
# ".bas",".bat",".bbs",".bfc",".bin",".bmp",".c",".cab",".cal",".cdf",".cdr",".cdx",".cfg",".chm",".clp"
# ".cmd",".cmf",".cnf",".cnt",".col",".com",".cpl",".cpp",".crd",".crt",".cur",".css",".dat",".dbf",".dcx"
# ".ddi",".dev",".dib",".dir",".dll",".doc",".dos",".dot",".drv",".dwg",".dxb",".dxf",".der",".dic",".emf"
# ".eps",".err",".exe",".exp",".exc",".flc",".fnd",".fon",".for",".fot",".fp",".fpt",".frt",".frx",".fxp"
# ".gif",".grh",".grp",".goc",".gra",".h",".hlp",".hqx",".ht",".htm",".html",".icm",".ico",".idf",".idx"
# ".iff",".image",".ime",".img",".inc",".inf",".ini",".jar",".jpeg",".jpg",".lnk",".log",".lzh",".mac",".mag"
# ".mdb",".men",".mid",".mif",".mov",".movie",".mp3",".mpg",".mpt",".msg",".obj",".ovl",".pcd",".pcs",".pcx"
# ".pdf",".psd",".pwl",".qt",".qtm",".rec",".reg",".rle",".rm",".rmi",".rtf",".sav",".scp",".scr",".sct"
# ".scx",".set",".shb",".snd",".sql",".svg",".svx",".swf",".swg",".sys",".tbk",".tga",".tiff",".tmp",".txt"
# ".url",".vcd",".ver",".voc",".vxd",".wab",".wav",".win",".wmf",".wpc",".wps",".wri",".xab",".xbm",".zip"
# ".a",".aam",".aas",".abf",".abk",".abs",".ace",".acl",".acp",".acr",".act",".acv",".ad",".ada",".adb"
# ".add",".adf",".adi",".adm",".adp",".adr",".ads",".afm",".af2",".af3",".ai",".aim",".ais",".akw",".alaw"
# ".alb",".all",".ams",".anc",".ant",".api",".apr",".aps",".ari",".art",".asa",".asc",".asd",".ase",".asm"
# ".aso",".ast",".asv",".att",".atw",".avb",".avr",".avs",".awd",".awr",".axx",".a3l",".a4l",".a5l",".a3m"
# ".a4m",".a4p",".a3w",".a4w",".a5w",".bdf",".bg",".bgl",".bi",".bif",".biff",".bk",".bk$",".bks",".bmk"
# ".bmi",".book",".box",".bpl",".bqy",".brx",".bsc",".bsp",".bs1",".bs_",".btm",".bud",".bun",".bw",".bwv"
# ".byu",".b4",".c0l",".cad",".cam",".cap",".cas",".cat",".cb",".cbi",".cc",".cca",".ccb",".ccf",".cch"
# ".ccm",".cco",".cct",".cda",".cdi",".cdm",".cdt",".cel",".cer",".cfb",".cfm",".cgi",".cgm",".ch",".chk"
# ".chr",".chp",".cht",".cif",".cil",".cim",".cin",".ck1",".ck2",".ck3",".ck4",".ck5",".ck6",".class",".cll"
# ".cls",".cmg",".cmp",".cmv",".cmx",".cnm",".cnq",".cob",".cod",".cpd",".cpe",".cpi",".cpo",".cpr",".cpt"
# ".cpx",".crp",".csc",".csp",".cst",".csv",".ct",".ctl",".cue",".cut",".cv",".cwk",".cws",".cxt",".cxx"
# ".db",".dbc",".dbx",".dcm",".dcr",".dcs",".dct",".dcu",".dc5",".ddf",".ddif",".def",".defi",".dem",".dewf"
# ".dgn",".dif",".dig",".diz",".dlg",".dls",".dmd",".dmf",".dpl",".dpr",".draw",".drw",".dsf",".dsg",".dsm"
# ".dsp",".dsq",".dst",".dsw",".dta",".dtd",".dted",".dtf",".dtm",".dun",".dv",".dwd",".dxr",".d64",".eda"
# ".edd",".ede",".edk",".edq",".eds",".edv",".efa",".efe",".efk",".efq",".efs",".efv",".emd",".eml",".enc"
# ".enff",".ephtml",".epsf",".eri",".epx",".esps",".eui",".evy",".ewl",".f",".f2r",".f3r",".f77",".f90",".far"
# ".fav",".fax",".fbk",".fcd",".fdb",".fdf",".fem",".ffa",".ffl",".ffo",".ffk",".fff",".fft",".fh3",".fif"
# ".fig",".fits",".fla",".flf",".fli",".flt",".fm",".fmb",".fml",".fmt",".fmx",".fng",".fnk",".fog",".fp1"
# ".fp3",".fpx",".frm",".fsf",".fsl",".fsm",".ft",".ftg",".fts",".fw2",".fw3",".fw4",".fzb",".fzf",".fzv"
# ".g721",".g723",".gal",".gcd",".gcp",".gdb",".gdm",".ged",".gem",".gen",".getright",".gfc",".gfi",".gfx",".gho"
# ".gid",".gim",".gix",".gkh",".gks",".gl",".gna",".gnt",".gnx",".grd",".grf",".gsm",".gtk",".gt2",".gwx"
# ".gwz",".gz",".hcm",".hcom",".hcr",".hdf",".hed",".hel",".hex",".hgl",".hh",".hog",".hpj",".hpp",".hst"
# ".htt",".htx",".hxm",".ica",".icb",".icc",".icl",".idb",".idd",".idq",".iges",".igf",".iif",".ilbm",".ima"
# ".imz",".inp",".inrs",".ins",".int",".iof",".iqy",".iso",".isp",".ist",".isu",".it",".iti",".its",".iv"
# ".ivd",".ivp",".ivt",".ivx",".iw",".iwc",".j62",".java",".jbf",".jff",".jfif",".jif",".jmp",".jn1",".jpe"
# ".js",".jsp",".jtf",".k25",".kar",".kdc",".key",".kfx",".kiz",".kkw",".kmp",".kqp",".kr1",".krz",".ksf"
# ".kye",".lab",".lbm",".lbt",".lbx",".ldb",".ldl",".leg",".les",".lft",".lgo",".lha",".lib",".lin",".lis"
# ".llx",".lpd",".lrc",".lsl",".lsp",".lst",".lu",".lvl",".lwlo",".lwob",".lwp",".lwsc",".lyr",".lzs",".m1v"
# ".m3d",".m3u",".mad",".maf",".magic",".mak",".mam",".man",".map",".maq",".mar",".mas",".mat",".maud",".max"
# ".maz",".mb1",".mbox",".mbx",".mcc",".mcp",".mcr",".mcw",".mda",".mde",".mdl",".mdn",".mdw",".mdz",".med"
# ".mer",".met",".mfg",".mgf",".mhtm",".mhtml",".mi",".mic",".miff",".mim",".mime",".mme",".mli",".mmf",".mmg"
# ".mmm",".mmp",".mn2",".mnd",".mni",".mng",".mnt,mnx",".mnu",".mod",".mp2",".mpa",".mpe",".mpeg",".mpp",".mpr"
# ".mri",".msa",".msdl",".msi",".msn",".msp",".mst",".mtm",".mul",".mus",".mus10",".mvb",".mwp",".nan",".nap"
# ".ncb",".ncd",".ncf",".ndo",".netcdf",".nff",".nft",".nil",".nist",".nlb",".nlm",".nls",".nlu",".nod",".nsf"
# ".nso",".nst",".ns2",".ntf",".ntx",".nwc",".nws",".o01",".obd",".obz",".ocx",".ods",".off",".ofn",".oft"
# ".okt",".olb",".ole",".oogl",".opl",".opo",".opt",".opx",".ora",".orc",".org",".or2",".or3",".oss",".ost"
# ".otl",".out",".p3",".p10",".p65",".p7c",".pab",".pac",".pak",".pal",".part",".pas",".pat",".pbd",".pbf"
# ".pbk",".pbl",".pbm",".pbr",".pce",".pcl",".pcm",".pcp",".pct",".pdb",".pdd",".pdp",".pdq",".pds",".pf"
# ".pfa",".pfb",".pfc",".pfm",".pgd",".pgl",".pgm",".pgp",".ph",".php",".php3",".phtml",".pic",".pict",".pif"
# ".pig",".pin",".pix",".pj",".pjx",".pjt",".pkg",".pkr",".pl",".plg",".pli",".plm",".pls",".plt",".pm5"
# ".pm6",".png",".pnt",".pntg",".pog",".pol",".pop",".pot",".pov",".pp4",".ppa",".ppf",".ppm",".ppp",".pps"
# ".ppt",".pqi",".prc",".pre",".prf",".prg",".prj",".prn",".prp",".prs",".prt",".prv",".prz",".ps",".psb"
# ".psi",".psm",".psp",".pst",".ptd",".ptm",".pub",".pwd",".pwp",".pwz",".pxl",".py",".pyc",".qad",".qbw"
# ".qdt",".qd3d",".qfl",".qic",".qif",".qlb",".qm",".qry",".qst",".qti",".qtif",".qtp",".qts",".qtx",".qw"
# ".qxd",".ra",".ram",".rar",".ras",".raw",".rbh",".rdf",".rdl",".rep",".res",".rft",".rgb",".sgi",".rl2"
# ".rmd",".rmf",".rom",".rov",".rpm",".rpt",".rrs",".rsl",".rsm",".rtk",".rtm",".rts",".rul",".rvp",".rxx"
# ".s",".s3i",".s3m",".sam",".sb",".sbk",".sbl",".sc2",".sc3",".scc",".scd",".scf",".sch",".sci",".scn"
# ".sct01",".scv",".sd",".sd2",".sdf",".sdk",".sdl",".sdr",".sds",".sdt",".sdv",".sdw",".sdx",".sea",".sep"
# ".ses",".sf",".sf2",".sfd",".sfi",".sfr",".sfw",".sfx",".sgml",".shg",".shp",".shs",".shtml",".shw",".sig"
# ".sit",".siz",".ska",".skl",".sl",".slb",".sld",".slk",".sm3",".smp",".sndr",".sndt",".sou",".spd",".spl"
# ".sppack",".sprite",".sqc",".sqr",".ssdo1",".ssd",".ssf",".st",".stl",".stm",".str",".sty",".sw",".swa",".swp"
# ".syw",".t64",".tab",".tar",".taz",".tcl",".tdb",".tddd",".tex",".tgz",".theme",".thn",".tif",".tig",".tlb"
# ".tle",".toc",".tol",".tos",".tpl",".tpp",".trk",".trm",".trn",".ttf",".ttk",".twf",".tww",".tx8",".txb"
# ".txw",".tz",".t2t",".ub",".udf",".udw",".ulaw",".ult",".uni",".use",".uu",".uue",".uw",".uwf",".v8"
# ".vap",".vba",".vbp",".vbw",".vbx",".vce",".vcf",".vct",".vcx",".vda",".vi",".viff",".vir",".viv",".viz"
# ".vlb",".vmf",".vox",".vp",".vqe",".vql",".vqf",".vrf",".vrml",".vsd",".vsl",".vsn",".vss",".vst",".vsw"
# ".w3l",".wad",".wal",".wb1",".wb2",".wbk",".wbl",".wbr",".wbt",".wcm",".wdb",".wdg",".web",".wfb",".wfd"
# ".wfm",".wfn",".wfp",".wgp",".wid",".wil",".wiz",".wk1",".wk3",".wk4",".wks",".wld",".wlf",".wll",".wow"
# ".wp",".wp4",".wp5",".wp6",".wpd",".wpf",".wpg",".wpt",".wpw",".wq1",".wq2",".wr1",".wrg",".wrk",".wrl"
# ".wrz",".ws1",".ws2",".ws3",".ws4",".ws5",".ws6",".ws7",".wsd",".wvl",".wwl",".x",".xar",".xi",".xif"
# ".xla",".xlb",".xlc",".xld",".xlk",".xll",".xlm",".xls",".xlt",".xlv",".xlw",".xm",".xnk",".xpm",".xr1"
# ".xtp",".xwd",".xwf",".xy3",".xy4",".xyp",".xyw",".x16",".x32",".yal",".ybk",".z",".zap",".zoo",
# ]