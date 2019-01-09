# Menselijke spraak en computers: *Waarom een computer het zo moeilijk heeft om te leren wat een kind zonder moeite voor elkaar krijgt*
####Yannick Jadoul en Marnix Van Soom -- Artificial Intelligence Lab, Vrije Universiteit Brussel

Je hebt het je hoogstwaarschijnlijk wel al eens afgevraagd. Waarom lijkt je smartphone jou nooit zo goed te verstaan als de persoon waarmee je daarnet aan het praten was? Hoe komt het toch dat je best iets trager en duidelijker spreekt tegen die computer in je hand dan in een normale conversatie? En in een luidruchtige omgeving is het waarschijnlijk al helemaal hopeloos om te verwachten dat je wordt verstaan door die smartphone.

Het antwoord ligt in het paradoxale besef dat menselijke spraak veel meer informatie bevat dan je eigenlijk denkt, maar tegelijkertijd soms ook veel minder. Om dat te verklaren, is het interessant om eens te kijken naar de eigenlijke geluidsgolven van een stuk gesproken tekst.

## Geluidsgolven en een hele berg aan informatie

Een vaakgebruikte voorbeeldtekst in de taalkunde, en meerbepaald in de fonetiek, is een fabel van Aesopus, "De Noordenwind en de Zon", die wordt vertaald en voorgelezen in verschillende talen. In het Nederlands gaat en klinkt dit als volgt:<sup>[1](#footnote-1)</sup>

<audio controls><source src="de_noordenwind_en_de_zon.wav" type='audio/wav' />Your browser does not support the audio tag.</audio>

Wat je hoort wanneer dit audiofragment afspeelt - en wat de computer opneemt wanneer die probeert te verstaan wat je zegt - is geluid, bestaande uit golven in de lucht. Als we die veranderende druk in een grafiek weergeven, ziet dat er zo uit voor de eerste zin van onze voorgelezen fabel:

<!-- insert wave.html -->
![](wave.png)
*(je kan inzoomen door te scrollen en de grafiek rondbewegen door hem te verslepen van links naar rechts)*

Wanneer we inzoomen op de *o* in "n**oo**rdenwind", kun je zien waarom we over golven spreken:

<!-- insert wave_detail.html -->
![](wave_detail.png)

In principe kan je stellen dat de vorm van deze golven het verschil maakt tussen verschillende klanken. Maar elke keer je een klank uitspreekt ziet die er natuurlijk net iets anders uit.

Als we dan de *o* uit "er**o**ver" onder de loep nemen, zie je hoe verschillend de geluidsgolven van dezelfde klank wel niet kunnen zijn:

<!-- insert wave_detail_bis.html -->
![](wave_detail_bis.png)

Een andere manier om geluid te visualiseren is door de frequenties in het geluid weer te geven. De sterkte van de verschillende frequenties verandert doorheen de tijd, afhankelijk van de verschillende klanken. Dit is eigenlijk ook wat het slakkenhuis-orgaan in je oor doet. Een afbeelding die aan de hand van kleur deze sterktes visualiseert wordt een spectrogram genoemd:

![](spectrogram.png)

Zie je die horizonaal golvende lijnen aan de onderkant van de afbeelding? Deze lijnen corresponderen met de toonhoogte van het geluid: als je goed oplet hoor je in het begin van "*de noordenwind*" de toon omhoog gaan, en dit zie je dan ook in helemaal links in de afbeelding. Het soort klank en de klankkleur wordt dan weer bepaald door de sterktes van deze lijnen en de rest van wat je kan zien in het spectrogram.

Maar verder kan je ook opmerken hoe complex het geluid van spraak wel niet is: als je spreekt maak je geen echte duidelijke letters, maar een soort continu veranderend signaal. Je ziet ook wel gelijkenissen tussen verschillende stukken, maar elke keer is het net iets anders en moeten je hersenen toch uitvogelen welke klank je net gehoord hebt.

Er zit in spraak ook een hoop informatie in waar misschien niet direct aan denkt. Je kan bijvoorbeeld horen of iemand ziek is, opgewekt of net teleurgesteld, of kwaad. En je hoort het wanneer iemand de vorige dag iets te hard meegezongen heeft op een concert en nu hees is. Je kan ook nadruk leggen op een bepaald woord in een uitgesproken zin. En tenslotte kan je met zelfs maar een paar woorden ook herkennen wie er tegen je sprak.

Dit is het eerste stuk van de paradox: er zit een hele hoop informatie in een gesproken zin of tekst; veel meer dan je je eigenlijk van dag tot dag realiseert. En een computer die daar enkel maar de zin "Wat voor weer wordt het morgen?" uit wil halen, moet verteld worden of leren hoe net enkel deze informatie uit die geluidsgolven te halen.


## Ambiguïteit en interpretatie

Door onderzoek in artificial intelligence, machine learning en spraakherkennning zijn computers tegenwoordig best goed in het leren onderscheiden van interessante en niet-relevante stukken van de data. Dus tot op zekere hoogte geraakt het bovenstaande probleem beetje bij beetje opgelost.

Er is echter een ander probleem met gesproken taal: eigenlijk zit niet álle nodige informatie duidelijk in de spraakgolven of spectrogrammen die we hierboven toonden. Zo kan je bijvoorbeeld niet de lippen zien bewegen waarmee dit geluid werd uitgesproken, noch de gelaatsuitdrukking. Wanneer het een goede opname is en de uitspraak duidelijk is, is dit geen probleem dat je dit als mens niet ziet. Maar hoeveel moeilijker is het een telefoongesprek te voeren in een luidruchtige omgeving, ten opzichte van een direct gesprek met een persoon die tegenover je zit? Dan opeens wordt het gezicht van de andere persoon kostbare informatie die je (onbewust) toelaat om de stukken die je eigenlijk niet verstaan hebt toch te kunnen interpreteren. Meer nog, uit onderzoek is gebleken dat de bewegingen die de lippen maken je hersenen kunnen doen geloven dat er een andere klankt wordt uitgesproken. Dit wordt het McGurk-effect genoemd, zoals in deze video geïllustreerd wordt:<sup>[2](#footnote-2)</sup>

<!-- <iframe width="560" height="315" src="https://www.youtube.com/embed/G-lN8vWm3m0?start=32&end=69" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe> -->

Daarnaast zijn er nog andere dingen die je niet zal terugvinden in het spraaksignaal zelf. Je hersenen proberen de woorden die je hoort te integreren met alle andere informatie die je hebt over de mogelijke betekenis. Bij een ietswat slordige uitspraak of een uitspraak met een vreemd dialect van de zin "De onderzoeker gaf haar collega een hand." zal je een uitgesproken "h**e**nd" kunnen corrigeren als onbestaand en "h**o**nd" als erg onwaarschijnlijk voor deze context. Het indrukwekkende is dat je dikwijls doet zonder dat je je ervan bewust bent.

Ter illustratie van de ambiguïteit die aanwezig kan zijn en onbewust wordt opgelost, kunnen we naar het volgende fragment luisteren. Wat hoor je?

<audio controls><source src="yanny_laurel.wav" type='audio/wav' />Your browser does not support the audio tag.</audio>

Dit audiofragment deed in het voorjaar van 2018 de ronde op internet en sociale media. Sommige mensen horen zonder twijfel "*Yanny*", terwijl de andere helft net zo zeker is "*Laurel*" te horen. Op de één of andere manier hangt het van je impliciete verwachtingen hoe je dit geluid zal interpreteren, terwijl geen van beide opties echt helemaal duidelijk is op basis van de geluidsgolven alleen.

Zo komen we tot het andere aspect waarom spraak zo moeilijk te verstaan is voor computers: een deel van de informatie ontbreekt. De eigenlijke betekenis van een gesproken zin hangt niet enkel af van het geluid dat je hoort, maar wordt ook gedeeltelijk door de menselijke verstaander afgeleid uit de context, verwachtingen en wereldkennis. Ook hier wordt verder onderzoek gedaan in de kunstmatige intelligentie over hoe je deze verschillende aspecten van intelligentie kan integreren, in tegenstelling tot enkel een nauwe taak op te lossen zoals 'katten herkennen in afbeeldingen'. Die grote doorbraak lijkt voorlopig echter nog even op zich te laten wachten.

Daarom bestuderen we in het Artificial Intelligence Lab van de VUB onder andere hoe computers net als mensen taal kunnen leren. Aan de ene kant komen we zo meer te weten over hoe taal en spraak onstaat, hoe het geleerd wordt door kinderen en hoe het menselijk brein hiermee omgaat. Tegelijkertijd kunnen deze inzichten er voor zorgen dat al die computers om je heen in de toekomst op een meer natuurlijke, meer menselijke manier zullen kunnen communiceren.

En ondertussen... mag je er eigenlijk van versteld staan hoe goed mensen elkaar kunnen verstaan, wanneer we dit soort ingewikkelde geluidsgolven door de lucht sturen. En misschien een beetje medelijden hebben met je smartphone, wanneer je er net iets duidelijker tegen moet praten om die ogenschijnlijk simpele taak te volbrengen?

<hr>

<a name="footnote-1">1</a>: Audioframent afkomstig uit het *Aesop Language Bank* project ([http://aesoplanguagebank.com/nl.html](http://aesoplanguagebank.com/nl.html)), ingesproken door Goedele Vermaelen in 2008, met dank aan Kenneth von Zeipel voor het gebruik van dit fragment.
<a name="footnote-2">2</a>: Videofragment afkomstig van het YouTube-kanaal van BBC, oorspronkelijk afkomstig uit een BBC2 documentaire "Horizon: Is Seeing Believing?".

