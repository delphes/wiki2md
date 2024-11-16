import os
import re
import requests
from bs4 import BeautifulSoup

base = "https://cp3.irmp.ucl.ac.be"

wiki = "/projects/delphes/wiki"
source = "/projects/delphes/browser"
attachement = "/projects/delphes/raw-attachment"

arxiv = "https?://arxiv.org/abs"
fastjet = "https?://fastjet.fr"

directory = "html"

pages = [
    "WikiStart",
    "Contact",
    "Releases",
    "WorkBook",
    "WorkBook/Arrays",
    "WorkBook/Candidate",
    "WorkBook/ConfigFile",
    "WorkBook/DataFlowDiagram",
    "WorkBook/DelphesAnalysis",
    "WorkBook/EventDisplay",
    "WorkBook/ExternalFastJet",
    "WorkBook/LibraryInterface",
    "WorkBook/Modules",
    "WorkBook/ModuleSystem",
    "WorkBook/PileUp",
    "WorkBook/Pythia8",
    "WorkBook/QuickTour",
    "WorkBook/ReadingCMSFiles",
    "WorkBook/RootTreeDescription",
    "WorkBook/Tutorials",
    "WorkBook/TutorialBologna",
    "WorkBook/Tutorials/Hefei",
    "WorkBook/Tutorials/Mc4Bsm",
    "WorkBook/Tutorials/Pisa",
    "WorkBook/Tutorials/Prefit",
    "WorkBook/Tutorials/Student",
]

subs = {
    r"WikiStart": r"index",
    r"WorkBook$": r"WorkBook/index",
    r"Tutorials$": r"Tutorials/index",
    r"TutorialBologna": r"Tutorials/Bologna",
    r"WorkBook/Tutorials": r"Tutorials",
    r"CMSFiles": r"CmsFiles",
    r"FastJet": r"Fastjet",
    r"WorkBook": r"workbook",
    r"([a-z])([A-Z])": r"\1-\2",
}

map = {}
for p in pages:
    f = p
    for pattern, repl in subs.items():
        f = re.sub(pattern, repl, f)
    f = f.lower()
    map[p] = f + ".html"

for page, file in map.items():
    r = requests.get(base + "/" + wiki + "/" + page)
    s = BeautifulSoup(r.content, "html.parser")
    d = s.find("div", {"id": "wikipage"})
    for tag in d.find_all("a", {"class": "trac-rawlink"}):
        tag.decompose()
    for tag in d.find_all("div", {"class": "wiki-toc"}):
        tag.decompose()
    for tag in d.find_all("span", {"class": "icon"}):
        tag.decompose()
    for tag in d.find_all("div"):
        tag.unwrap()
    for tag in d.find_all("span"):
        tag.unwrap()
    for attr in ["class", "id", "rel", "title", "width"]:
        for tag in d.find_all(attrs={attr: True}):
            del tag[attr]
    for i in d.find_all("img", attrs={"src": True}):
        src = i["src"]
        src = re.sub(attachement + ".*/", "/etc/", src)
        i["src"] = src
    for a in d.find_all("a", attrs={"href": True}):
        i = a.find("img")
        if i:
            a.replace_with(i)
            continue
        href = a["href"].strip()
        text = a.string.strip()
        href = re.sub(base, "", href)
        href = re.sub(source, "$source$", href)
        href = re.sub(attachement + ".*/", "/etc/", href)
        href = re.sub(arxiv, "$arxiv$", href)
        href = re.sub(fastjet, "$fastjet$", href)
        text = text.replace(base, "")
        for p, f in map.items():
            f = re.sub("/*index.html", "", f)
            f = re.sub("\.html", "", f)
            href = re.sub(wiki + "/" + p + "$", "/" + f, href)
            text = re.sub(wiki + "/" + p + "$", "/" + f, text)
        text = re.sub("WorkBook/", "", text)
        text = re.sub("WorkBook", "Workbook", text)
        a["href"] = href
        a.string = text
    path = os.path.join(directory, file)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as output:
        output.write(d.renderContents())
