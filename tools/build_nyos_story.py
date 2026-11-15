"""Author the Lake Nyos script and research-backed storyboard for cinematic-film."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'projects/lake-nyos/film'
chapters=[
('The invisible disaster','1986',[
('On an August evening in nineteen eighty-six, a lake in Cameroon released an invisible danger.','archival lake photograph in darkness','CAMEROON / 1986','S1'),
('People did not have to touch the water.','camera moves from lake toward a schematic valley','BEYOND THE SHORE','S1'),
('The danger travelled through the air.','thin shaded gas layer follows the valley floor','ILLUSTRATIVE RECONSTRUCTION','S1'),
('More than seventeen hundred people died.','hold on a restrained casualty statement','MORE THAN 1,700 LIVES','S2'),
('The main killer was not floodwater, fire, or a flow of lava.','three simple hazards recede, leaving the lake','AN INVISIBLE HAZARD','S2'),
('It was carbon dioxide, released from the lake itself.','lake section reveals the gas reservoir','CO2','S2'),
('How can a lake make the air around it deadly?','pull back from valley to the lake and title','THE LAKE THAT EXHALED','S1'),
('The answer begins beneath a surface that hides what is happening below.','camera crosses the surface into the section diagram','BELOW THE SURFACE','S3'),
]),
('A reservoir beneath the water','background',[
('Lake Nyos lies in northwestern Cameroon, in a landscape shaped by volcanic activity.','Africa and Cameroon locator map','LAKE NYOS / CAMEROON','S1'),
('The lake occupies a crater, but its water holds a less obvious connection to the ground.','NASA satellite photograph with crater outline','CRATER LAKE','S1'),
('Carbon dioxide from deep geological sources enters the lake with groundwater.','subsurface flow paths, labelled schematic','GAS-BEARING GROUNDWATER','S1'),
('Here, the gas can dissolve in water, rather than immediately escaping into the sky.','molecule marks become dispersed through deep water','DISSOLVED GAS','S4'),
('Imagine a bottle of sparkling water before you open it.','a small neutral bottle illustration next to the section','A PRESSURE ANALOGY','S4'),
('The liquid can hold gas that is not visible as a cloud of bubbles.','bottle detail: dissolved marks, no enormous bubble','HELD IN SOLUTION','S4'),
('At Nyos, the weight of the water above helps keep gas dissolved at depth.','water column with downward pressure arrows','PRESSURE INCREASES WITH DEPTH','S4'),
('The other part of the trap is the way the lake mixes.','cross section divides into upper and lower layers','SEPARATE LAYERS','S3'),
('The surface can change while much deeper water remains isolated beneath it.','animated upper currents above quiet lower water','SURFACE / DEEP WATER','S3'),
('Weak deep mixing allows dissolved carbon dioxide to accumulate in the lower layers.','progressively denser dissolved-gas markers','GAS ACCUMULATES','S3'),
('That does not mean every deep lake is waiting to do the same thing.','ordinary lake outlines fade behind highlighted exceptional case','AN UNUSUAL COMBINATION','S3'),
('Nyos combined a continuing gas supply with water that could store it.','two pathways converge on one deep reservoir','SUPPLY + STORAGE','S3'),
('The important quantity was hidden below the surface, not written across the landscape.','satellite surface overlaid with a section window','A HIDDEN RESERVOIR','S3'),
]),
('When pressure falls','mechanism',[
('Now imagine some of that gas-rich deep water moving upward.','a highlighted parcel rises through the column','UPWARD MOVEMENT','S4'),
('As it rises, less water presses down on it.','pressure arrows shorten above the rising parcel','PRESSURE FALLS','S4'),
('Gas can then come out of solution and form bubbles.','dispersed marks gather into expanding circles','BUBBLES FORM','S4'),
('The analogy is opening that bottle: reduce the pressure, and the gas escapes.','bottle cap lifts beside matching rising bubbles','PRESSURE RELEASE','S4'),
('But the lake contains a much larger reservoir than a bottle on a table.','camera pulls back to the entire deep lake','A LAKE-SCALE RESERVOIR','S4'),
('As bubbles expand, they can lift more water upward.','bubble plume carries rising water arrows','BUBBLES LIFT WATER','S5'),
('That water encounters lower pressure, allowing more gas to separate from the liquid.','next parcel enters the plume','MORE GAS ESCAPES','S5'),
('More rising water can mean more bubbles, and more bubbles can mean more rising water.','a restrained feedback loop animates over the section','A SELF-REINFORCING RELEASE','S5'),
('A slow accumulation can become a rapid release.','reservoir changes from dissolved markers to an outward plume','SLOW BUILDUP / RAPID RELEASE','S5'),
('Scientists call this type of lake gas outburst a limnic eruption.','scientific term appears beside the mechanism','LIMNIC ERUPTION','S5'),
('The word eruption can be misleading if it makes us picture a volcano throwing out lava.','small lava icon crosses out, gas pathway remains','GAS, NOT A LAVA FLOW','S2'),
('The investigation found no significant direct volcanic activity responsible for the disaster.','evidence note backed by the investigation reference','INVESTIGATION: 1987','S2'),
('The gas had been stored in the water. The lake released that stored danger.','camera returns to dissolved reservoir and upward path','STORED IN THE LAKE','S2'),
]),
('A cloud follows the land','1986',[
('Once outside the water, the gas became a different kind of threat.','cross section transitions to landscape profile','ABOVE THE WATER','S1'),
('A concentrated carbon dioxide cloud is denser than the surrounding air.','dense gas shading rests below lighter air','DENSER THAN AIR','S6'),
('It can flow downhill and collect in low ground.','arrows follow the lower valley contour','DOWNHILL','S6'),
('The landscape that channels water can also help channel this invisible gas.','compare water route and gas route without drawing a flood','TERRAIN GUIDES THE FLOW','S6'),
('Carbon dioxide is part of ordinary air. At high concentrations, it is dangerous.','normal versus concentrated schematic molecule density','CONCENTRATION MATTERS','S6'),
('Near Nyos, people died from carbon dioxide asphyxiation.','restrained text on the human impact, no bodies','THE HUMAN COST','S2'),
('The catastrophe reached communities beyond the lake shore.','schematic settlement markers downstream, no exact village layout','COMMUNITIES DOWNSTREAM','S7'),
('NASA describes deadly effects as far as twenty-five kilometres away.','distance marker labelled reported extent rather than exact boundary','REPORTED EFFECTS: UP TO 25 KM','S7'),
('That distance is a reminder: this was not simply an accident confined to the water.','pull back across lake, valley and community markers','ONE CONNECTED LANDSCAPE','S7'),
('And an invisible gas gives no visible boundary for a person to recognize.','shaded diagram layer switches to a transparent contour','GAS SHADING IS AN ILLUSTRATION','S6'),
]),
('What the evidence can tell us','investigation',[
('After the disaster, researchers had to distinguish several possible explanations.','investigation board with a lake section and samples','FOLLOWING THE EVIDENCE','S2'),
('They studied the lake water, the gases, and the geological setting.','water-sample, gas-sample and geology symbols linked to source','WATER / GAS / GEOLOGY','S2'),
('Their evidence identified carbon dioxide and connected its origin to deep magmatic sources.','source path connects earth to dissolved gas','DEEP GEOLOGICAL ORIGIN','S2'),
('But the source of the gas is not the same question as the trigger.','separate origin and trigger pathways','ORIGIN IS NOT TRIGGER','S8'),
('What precisely started the release that night remains uncertain.','an open question sits at the start of the mechanism','PRECISE TRIGGER: UNCERTAIN','S8'),
('Researchers have proposed different mechanisms for disturbing or destabilizing gas-rich water.','several lightly drawn possible disturbances, marked hypotheses','PROPOSED MECHANISMS','S8'),
('A diagram can explain how a release grows without proving which trigger actually occurred.','mechanism solid line; initiating event dashed line','MECHANISM / UNCERTAINTY','S8'),
('So we should not present one dramatic landslide or earthquake as an established scene.','hypothesis icons recede instead of staged disaster footage','DO NOT INVENT CERTAINTY','S8'),
('The evidence supports the reservoir and the release. The exact first push is another matter.','return to confirmed reservoir and outflow with open starting node','KNOWN / NOT ESTABLISHED','S8'),
('There was also a practical question: how could the stored gas be removed more safely?','camera follows reservoir toward a narrow pipe outline','FROM EXPLANATION TO PREVENTION','S9'),
]),
('Letting the lake breathe','2001 onward',[
('Controlled degassing began at Lake Nyos in two thousand and one.','archival 2001 degassing photograph','CONTROLLED DEGASSING / 2001','S9'),
('A pipe draws gas-rich water from deep in the lake toward the surface.','section diagram with pipe intake in lower water','DEEP-WATER INTAKE','S9'),
('As the water rises inside, pressure drops and dissolved gas forms bubbles.','bubbles emerge progressively inside the pipe','CONTROLLED PRESSURE DROP','S9'),
('The expanding bubbles help lift the water, allowing the flow to sustain itself under suitable conditions.','upward flow reaches the outlet','GAS-LIFT FLOW','S9'),
('The pipe uses the same pressure change that makes an uncontrolled release dangerous.','compare bounded pipe flow to broad eruption plume','THE SAME PHYSICS','S9'),
('The difference is that gas is released through a controlled pathway.','pipe stays highlighted, surrounding reservoir remains contained','CONTROLLED RELEASE','S9'),
('Researchers measured the response rather than assuming the intervention was harmless.','measurement profiles appear beside the pipe','MEASURE / CHECK / ADJUST','S10'),
('Studies found gas reductions and no dangerous destabilization from the degassing they observed.','archival source identifiers beside a declining conceptual reservoir','OBSERVED REDUCTION','S10'),
('But gas can continue entering the lake, so removal is not a reason to stop monitoring.','inflow arrow remains while pipe removes gas','RECHARGE CONTINUES','S10'),
('This is a history of an engineering response, not a live safety assessment of Nyos today.','dated timeline ends without a present-day safety badge','HISTORICAL ACCOUNT','S10'),
('A lake can become deadly without sending a flood through a village.','return to calm lake image with transparent gas path','THE ANSWER WAS IN THE WATER','S1'),
('At Nyos, gas accumulated below, escaped upward, and moved into the air people were breathing.','whole explanatory board: supply, storage, release, terrain','SUPPLY / STORAGE / RELEASE','S5'),
('Understanding that hidden process made a response possible.','final pipe and reservoir connection','UNDERSTANDING CHANGES THE RESPONSE','S10'),
('The surface was only the part of the story we could see.','final close on archival lake surface, fade to credits','LAKE NYOS / REMEMBERING THOSE LOST','S1'),
])]
sources={
'S1':{'title':'NASA Science: Lake Nyos, Cameroon','url':'https://science.nasa.gov/earth-science/programs/research-analysis/lake-nyos-cameroon/','supports':'Date, northwestern Cameroon, crater, geological CO2 supply, broad event framing.'},
'S2':{'title':'Kling et al. (1987), Science: The 1986 Lake Nyos Gas Disaster','url':'https://pubmed.ncbi.nlm.nih.gov/17789781/','doi':'10.1126/science.236.4798.169','supports':'At least 1700 deaths, CO2 asphyxiation, dissolved reservoir, magmatic origin, no significant direct volcanic activity.'},
'S3':{'title':'Kling, Evans & Tanyileke (2015): Comparative limnology','url':'https://www.usgs.gov/publications/comparative-limnology-lakes-nyos-and-monoun-cameroon','supports':'Weak deep mixing, persistent lower-water isolation, gradual dissolved CO2 buildup; rarity.'},
'S4':{'title':'Zhang (1996): Dynamics of CO2-driven lake eruptions','url':'https://www.nature.com/articles/379057a0','doi':'10.1038/379057a0','supports':'Physical explanation of CO2-driven release; pressure/bubble mechanism. Bottle is an explanatory analogy, not an assertion of identical systems.'},
'S5':{'title':'Chan, Kwok & Mak (1996): A model of gas buildup and release in crater lakes','url':'https://hub.hku.hk/bitstream/10722/80916/1/content.pdf','supports':'Dissolved gas, release dynamics, triggering hypotheses; model-specific predictions not adopted.'},
'S6':{'title':'IPCC Special Report on Carbon Dioxide Capture and Storage, chapter 6, box 6.7','url':'https://archive.ipcc.ch/pdf/special-reports/srccs/srccs_chapter6.pdf','supports':'Lake Nyos CO2 hazard and its behaviour after release; general concentration/terrain explanation.'},
'S7':{'title':'NASA SVS: Lake Nyos Zoom-in (2002)','url':'https://svs.gsfc.nasa.gov/2348/','supports':'Reported deadly effects as far as 25 km; Landsat imagery dated 2001-02-05.'},
'S8':{'title':'Kling et al. (1987), full paper; and Cotel (1999), A trigger mechanism','url':'https://sites.lsa.umich.edu/gwk/wp-content/uploads/sites/647/2018/09/Kling_etal_Science1987.pdf','additional_url':'https://www.sciencedirect.com/science/article/pii/S0377027399000177','supports':'Trigger unknown in investigation; later proposed mechanisms remain hypotheses, not a witnessed reconstruction.'},
'S9':{'title':'Kling et al. (2005): Degassing Lakes Nyos and Monoun','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC1242283/','doi':'10.1073/pnas.0502274102','supports':'Nyos degassing started in 2001; gas removal, pipe operation and changing rates.'},
'S10':{'title':'USGS 2005 degassing findings and 2015 comparative limnology','url':'https://www.usgs.gov/publications/degassing-lakes-nyos-and-monoun-defusing-certain-disaster','additional_url':'https://www.usgs.gov/publications/comparative-limnology-lakes-nyos-and-monoun-cameroon','supports':'Measured gas reduction, no dangerous water-column destabilization observed; continued gas recharge and monitoring.'}
}
takes=[]; idx=1; md=['# How Can a Lake Kill Without Flooding?','', 'Working narration draft. Target: 6-8 minutes, English. Actual duration will follow the recorded voice.','']
boards=['# Storyboard and production plan','','Primary engine: cinematic-film (Skia). HyperFrames is optional support, not the primary renderer.','', '| Chapter | Planned visual sequence | Evidence boundary |','| --- | --- | --- |']
for ci,(name,era,rows) in enumerate(chapters,1):
    lines=[]; md+=['## '+str(ci)+'. '+name,'']
    for text,hero,typed,source in rows:
        lines.append({'id':idx,'text':text,'spoken':text,'hero':hero,'typed':typed,'source_ids':[source],'gap_after':0.42 if idx!=7 else 0.9})
        md.append(text+' ['+source+']'); idx+=1
    takes.append({'take':f'T{ci:02d}_'+name.lower().replace(' ','_'),'lines':lines})
    md.append('')
    boards.append(f'| {ci}. {name} | '+ ' → '.join(r[1] for r in rows[::3])+' | '+('Real imagery identified by date; schematic gas made visible only by illustrative shading' if ci in (1,2,4) else 'Schematic mechanisms; no asserted trigger or present-day safety claim')+' |')
story={'title':'How Can a Lake Kill Without Flooding?','takes':takes,'fact_notes':[k+': '+s['supports']+' '+s['url'] for k,s in sources.items()]}
(P/'script.json').write_text(json.dumps(story,indent=2,ensure_ascii=False),encoding='utf-8')
(P/'script.md').write_text('\n'.join(md),encoding='utf-8')
(P/'storyboard.md').write_text('\n'.join(boards)+'\n\nEvery narration line has a more detailed hero and on-screen text in script.json. Initial review targets the first 30-45 seconds at 1280x720, before committing to a full render.\n',encoding='utf-8')
(P/'sources.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
words=sum(len(l['spoken'].split()) for t in takes for l in t['lines'])
print(f'{len(takes)} sections; {idx-1} lines; {words} spoken words; '+str(P/'script.md'))
