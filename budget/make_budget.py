from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys
out=sys.argv[1]
F="Arial"
blue=Font(name=F,color="0000FF"); black=Font(name=F); bold=Font(name=F,bold=True)
hdr=Font(name=F,bold=True,color="FFFFFF"); hfill=PatternFill("solid",fgColor="3A3A3A")
yfill=PatternFill("solid",fgColor="FFF2B3"); gfill=PatternFill("solid",fgColor="EEEEEE")
EUR='€#,##0;(€#,##0);-'; EUR2='€#,##0.00;(€#,##0.00);-'
thin=Side(style="thin",color="BBBBBB")

Q="Quote"; L="Listed price"; E="Estimate"
lines=[
# node, item, qty, unit, basis, note, include
("Walls 1–4","Retired PV panel, 185 W class",4,30,E,"Second-hand / end-of-life panel; may be donated","Yes"),
("Walls 1–4","PVA carrier board v1, assembled, with ELEGOO ESP32, DS3231, probe",4,70,E,"Small-run assembly with SUNDIAL's order; confirm with the PCB maker's quote","Yes"),
("Walls 1–4","IP65 box, glands, breather vent",4,30,E,"As SUNDIAL (CARRIER.md: about 150 x 110 x 70 mm)","Yes"),
("Walls 1–4","Fixings, stand-offs, cable, fuse",4,40,E,"","Yes"),
("Walls 1–4","Wall plate: number, 5 x 5 logo, Wi-Fi QR",4,20,E,"","Yes"),

("Battery tier (5 interactive nodes)","Retired PV panel, 185 W class",5,30,E,"","Yes"),
("Battery tier (5 interactive nodes)","PVA carrier board v1, assembled",5,70,E,"","Yes"),
("Battery tier (5 interactive nodes)","Victron SmartSolar MPPT 75/15",5,102,L,"BigBuy, about €102 each for 6+ (Oct 2026)","Yes"),
("Battery tier (5 interactive nodes)","12 V LiFePO4 battery, 50 Ah",5,200,E,"Premium brand listed at €286 (Patona, Oct 2026); budget brands lower. Size per node in the pilot","Yes"),
("Battery tier (5 interactive nodes)","Equipment cabinet, IP65, for battery, MPPT and board",5,150,E,"","Yes"),
("Battery tier (5 interactive nodes)","Fuses, holders, cables, VE.Direct cable",5,50,E,"","Yes"),
("Battery tier (5 interactive nodes)","Mounting and fixings",5,50,E,"","Yes"),
("Battery tier (5 interactive nodes)","Wall plate",5,20,E,"","Yes"),

("Street auction","Three lit lockers: frame and perspex doors, fabricated",1,900,E,"Biggest unknown in this node: get a local fabricator's quote","Yes"),
("Street auction","Fail-secure solenoid locks",3,25,E,"","Yes"),
("Street auction","Door switches",3,5,E,"","Yes"),
("Street auction","LED strips and controller",1,80,E,"","Yes"),
("Street auction","Off-board driver (MOSFETs, relays)",1,30,E,"","Yes"),

("Arm game","Waveshare RoArm-M2-S",1,230,L,"About $205–225 (Amazon, AliExpress); RobotShop EU and Grobotronics stock it","Yes"),
("Arm game","12 V 5 A regulated DC-DC for the arm",1,25,E,"Arm takes 7–13 V; battery reaches 14.6 V","Yes"),
("Arm game","Perspex enclosure",1,350,E,"","Yes"),
("Arm game","Peg board, ramp, hopper, pegs",1,80,E,"","Yes"),
("Arm game","Hole sensors (IR break-beam)",5,3,E,"","Yes"),
("Arm game","Arm power switch (MOSFET or relay)",1,10,E,"","Yes"),

("Gettoneria","Coin hopper, Slomatic X3 EXP, 12 V, ccTalk",1,220,E,"No public price; a comparable ccTalk hopper is listed at $155. Ask Slomatic for a quote","Yes"),
("Gettoneria","Programmable coin acceptor",1,35,L,"CH-926 class listed at €31.40 (ArcadeXpress); a better acceptor for plastic tokens could be €100–200","Yes"),
("Gettoneria","NFC readers, PN532 class (exit, redeem, status pad)",3,10,E,"","Yes"),
("Gettoneria","I2C multiplexer, ccTalk interface, status light",1,20,E,"","Yes"),
("Gettoneria","Two-way flap solenoid and driver",1,20,E,"","Yes"),
("Gettoneria","Steel housing with slot, cups, reject box, reserve tube",1,450,E,"Local fabrication","Yes"),
("Gettoneria","Tokens: printed coin, NTAG213 tag, printed number, assembled",1000,1.0,E,"€0.50–1.50 each (interactive-token.md 2.7); 500 core + 500 buffer","Yes"),
("Gettoneria","USB NFC writer for batches (bench)",1,45,E,"","Yes"),

("Flip-dot wall","Alfa-Zeta XY5 14 x 28 panel, yellow on black, controller included",2,440,Q,"Alfa-Zeta quote, 23 Oct 2026","Yes"),
("Flip-dot wall","Alfa-Zeta shipping to Italy",1,25,Q,"Alfa-Zeta quote, 23 Oct 2026","Yes"),
("Flip-dot wall","12 V to 24 V converter, fixed output, about 2 A",1,45,E,"Mean Well SD-50A-24 class","Yes"),
("Flip-dot wall","RS-485 transceiver",1,5,E,"","Yes"),
("Flip-dot wall","Programmable coin acceptor",1,35,L,"As the gettoneria's","Yes"),
("Flip-dot wall","NFC reader and I2C port expander",1,15,E,"","Yes"),
("Flip-dot wall","Two-way flap solenoid and driver",1,20,E,"","Yes"),
("Flip-dot wall","Vandal-resistant rotary encoders and knobs",2,25,E,"","Yes"),
("Flip-dot wall","Vandal-resistant push button",1,20,E,"","Yes"),
("Flip-dot wall","Steel housing with glass window, about 480 x 470 x 100 mm inside",1,550,E,"Alfa-Zeta recommend steel and glass; local fabrication","Yes"),
("Flip-dot wall","Token column (perspex tube) and kept-token box",1,60,E,"","Yes"),
("Flip-dot wall","Spare dots",20,0.5,Q,"Alfa-Zeta, €0.50 a dot, 25 Oct 2026","Yes"),

("The SUNSET set","Outdoor Bluetooth speaker",1,180,E,"","Yes"),
("The SUNSET set","Speaker locker: perspex door, lock, door switch",1,250,E,"","Yes"),
("The SUNSET set","Speaker charger (12 V to USB/DC)",1,20,E,"","Yes"),

("Shared","Spare carrier board, assembled and keyed",1,70,E,"","Yes"),
("Shared","Spare 7 x 28 flip-dot module (bench piece now, spare later)",1,220,Q,"Alfa-Zeta quote, 23 Oct 2026","Yes"),
("Shared","Bench and development kit: ESP32s, readers, acceptor, sample tokens",1,150,E,"","Yes"),
("Shared","Shipping and import, all other orders",1,200,E,"","Yes"),
("Shared","Tools and consumables",1,100,E,"","Yes"),

("Garden node (option)","Steel post and base frame",1,450,E,"Replaces one wall's fixings; panel and board already counted in Walls","No"),
("Garden node (option)","Structural engineer's sign-off",1,400,E,"","No"),
("Garden node (option)","IBC tank, food-grade, opaque",1,150,E,"","No"),
("Garden node (option)","Wood cladding",1,150,E,"","No"),
("Garden node (option)","Pump, 12 V converter, soil probe, float switches, MOSFET",1,75,E,"","No"),
("Garden node (option)","Drip kit and planting",1,140,E,"","No"),

("Running, first year","Public liability insurance",1,400,E,"Get a quote; may be shared with SUNDIAL's policy","Yes"),
("Running, first year","Token top-up: souvenirs and losses",100,1.0,E,"","Yes"),
("Running, first year","Flip-dot upkeep: spare dots, compressed air",1,50,E,"","Yes"),
("Running, first year","Website hosting (GitHub Pages)",1,0,L,"Free","Yes"),
]
nodes=["Walls 1–4","Battery tier (5 interactive nodes)","Street auction","Arm game","Gettoneria","Flip-dot wall","The SUNSET set","Shared"]

wb=Workbook()
S=wb.active; S.title="Summary"
Lw=wb.create_sheet("Lines")
heads=["Node","Item","Qty","Unit (€)","Total (€)","Basis","Source / note","Include"]
for i,h in enumerate(heads,1):
    c=Lw.cell(1,i,h); c.font=hdr; c.fill=hfill
for r,(n,it,q,u,b,note,inc) in enumerate(lines,2):
    Lw.cell(r,1,n).font=black; Lw.cell(r,2,it).font=black
    c=Lw.cell(r,3,q); c.font=blue
    c=Lw.cell(r,4,u); c.font=blue; c.number_format=EUR2 if u<5 else EUR
    c=Lw.cell(r,5,f"=C{r}*D{r}"); c.font=black; c.number_format=EUR
    Lw.cell(r,6,b).font=black; Lw.cell(r,7,note).font=black
    c=Lw.cell(r,8,inc); c.font=blue
last=len(lines)+1
for col,w in zip("ABCDEFGH",[30,62,7,11,12,14,70,9]): Lw.column_dimensions[col].width=w
Lw.freeze_panes="A2"

S["A1"]="SUNSET: budget to build the nine panels"; S["A1"].font=Font(name=F,bold=True,size=14)
S["A2"]="Draft, 25 Oct 2026. Hardware and first-year running costs; PVA's own labour, travel and permit fees are not included."; S["A2"].font=black
S["A4"]="Node"; S["B4"]="Cost (€)"; S["C4"]="Share"
for c in ("A4","B4","C4"): S[c].font=hdr; S[c].fill=hfill
rng=f"Lines!$E$2:$E${last}"; nr=f"Lines!$A$2:$A${last}"; ir=f"Lines!$H$2:$H${last}"
r=5
for n in nodes:
    S.cell(r,1,n).font=black
    c=S.cell(r,2,f'=SUMIFS({rng},{nr},A{r},{ir},"Yes")'); c.font=black; c.number_format=EUR
    r+=1
first,lastn=5,r-1
S.cell(r,1,"Build subtotal").font=bold
c=S.cell(r,2,f"=SUM(B{first}:B{lastn})"); c.font=bold; c.number_format=EUR; sub=r
for rr in range(first,lastn+1):
    c=S.cell(rr,3,f"=IFERROR(B{rr}/$B${sub},0)"); c.font=black; c.number_format='0.0%'
r+=1
S.cell(r,1,"Contingency").font=black
cont=r
r+=1
S.cell(r,1,"Build total").font=bold
c=S.cell(r,2,f"=B{sub}+B{cont}"); c.font=bold; c.number_format=EUR; build=r
r+=1
S.cell(r,1,"Running, first year").font=black
c=S.cell(r,2,f'=SUMIFS({rng},{nr},"Running, first year",{ir},"Yes")'); c.font=black; c.number_format=EUR; run=r
r+=1
S.cell(r,1,"Total, build and first year").font=Font(name=F,bold=True,size=12)
c=S.cell(r,2,f"=B{build}+B{run}"); c.font=Font(name=F,bold=True,size=12); c.number_format=EUR; tot=r
for rr in (sub,build,tot):
    for cc in (1,2,3): S.cell(rr,cc).border=Border(top=thin)
r+=2
S.cell(r,1,"Contingency rate").font=black
c=S.cell(r,2,0.15); c.font=blue; c.fill=yfill; c.number_format='0%'
c=S.cell(cont,2,f"=B{sub}*B{r}"); c.font=black; c.number_format=EUR
r+=2
S.cell(r,1,"Option, not in the total:").font=bold; r+=1
S.cell(r,1,"Garden node (replaces one wall)").font=black
c=S.cell(r,2,f'=SUMIFS({rng},{nr},"Garden node (option)")'); c.font=black; c.number_format=EUR
r+=2
notes=["How to use it",
"Edit only the blue cells: quantities, unit prices and Include (Yes/No) on the Lines sheet, and the contingency rate above (yellow).",
"Basis on each line: Quote (from the supplier), Listed price (seen online, Oct 2026), Estimate (to be confirmed).",
"Prices include VAT where they are retail prices; Alfa-Zeta invoices B2B to an Italian VAT number (reverse charge).",
"To include the garden node, set its lines' Include to Yes on the Lines sheet.",
"Not included: PVA's labour, travel, permit and authorisation fees, and the token artwork."]
S.cell(r,1,notes[0]).font=bold
for t in notes[1:]:
    r+=1; S.cell(r,1,t).font=black
S.column_dimensions["A"].width=40; S.column_dimensions["B"].width=14; S.column_dimensions["C"].width=10
wb.save(out)
