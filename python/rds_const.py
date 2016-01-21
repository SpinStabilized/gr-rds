three_letter = { 39248: 'KEX',
                 39249: 'KFH',
                 39250: 'KFI',
                 39251: 'KGA',
                 39252: 'KGO',
                 39253: 'KGU',
                 39254: 'KGW',
                 39255: 'KGY',
                 39256: 'KID',
                 39257: 'KIT',
                 39258: 'KJR',
                 39259: 'KLO',
                 39260: 'KLZ',
                 39261: 'KMA',
                 39262: 'KMJ',
                 39263: 'KNX',
                 39264: 'KOA',
                 39268: 'KQV',
                 39269: 'KSL',
                 39270: 'KUJ',
                 39271: 'KVI',
                 39272: 'KWG',
                 39275: 'KYW',
                 39277: 'WBZ',
                 39278: 'WDZ',
                 39279: 'WEW',
                 39281: 'WGL',
                 39282: 'WGN',
                 39283: 'WGR',
                 39285: 'WHA',
                 39286: 'WHB',
                 39287: 'WHK',
                 39288: 'WHO',
                 39290: 'WIP',
                 39291: 'WJR',
                 39292: 'WKY',
                 39293: 'WLS',
                 39294: 'WLW',
                 39297: 'WOC',
                 39299: 'WOL',
                 39300: 'WOR',
                 39304: 'WWJ',
                 39305: 'WWL',
                 39312: 'KDB',
                 39313: 'KGB',
                 39314: 'KOY',
                 39315: 'KPQ',
                 39316: 'KSD',
                 39317: 'KUT',
                 39318: 'KXL',
                 39319: 'KXO',
                 39321: 'WBT',
                 39322: 'WGH',
                 39323: 'WGY',
                 39324: 'WHP',
                 39325: 'WIL',
                 39326: 'WMC',
                 39327: 'WMT',
                 39328: 'WOI',
                 39329: 'WOW',
                 39330: 'WRR',
                 39331: 'WSB',
                 39332: 'WSM',
                 39333: 'KBW',
                 39334: 'KCY',
                 39335: 'KDF',
                 39338: 'KHQ',
                 39339: 'KOB',
                 39347: 'WIS',
                 39348: 'WJW',
                 39349: 'WJZ',
                 39353: 'WRC'}

def callsign(pi):
	if pi[0:2] == 'AF':
		picode = pi[2:] + '00'

	if pi[0] == 'A':
		picode = pi[1] + '0' + pi[2:]

	picode = int(pi, 16)
	cs = ['','','','']
	if picode > 4095 and picode < 39247:
		if picode > 21671:
			cs[0] = 'W'
			picode = picode - 21672
		else:
			cs[0] = 'K'
			picode = picode - 4096

		cs[1] = picode // 676
		picode = picode - (676 * cs[1])
		cs[2] = picode // 26
		cs[3] = picode - (26 * cs[2])
		cs[1] = chr(cs[1] + ord('A'))
		cs[2] = chr(cs[2] + ord('A'))
		cs[3] = chr(cs[3] + ord('A'))
		cs = ''.join(cs)
	elif picode in three_letter.keys():
			cs = three_letter[picode]
	else:
		cs = 'ERR'

	return cs
