artoo.scrape('tr', {
  title: {sel: 'h3'},
  img: {sel: 'img', attr: 'src'},
  text: {sel: 'p:first'},
  description: {sel: 'i'},
  type: function() {
  	var text = 'none';
  	var info = $(this).find("li");
  	info.each(function() {
  		if($(this).text().substring(0,5) === 'Type:') {
  			 text = $(this).text().replace('Type:', '');
  		}
  	});
  	return text;
  },
  class: function() {
  	var text = 'none';
  	var info = $(this).find("li");
  	info.each(function() {
  		if($(this).text().substring(0,6) === 'Class:') {
  			 text = $(this).text().replace('Class:', '');
  		}
  	});
  	return text;
  },
  rarity: function() {
  	var text = 'none';
  	var info = $(this).find("li");
  	info.each(function() {
  		if($(this).text().substring(0,7) === 'Rarity:') {
  			 text = $(this).text().replace('Rarity:', '');
  		}
  	});
  	return text;
  },
  set: function() {
  	var text = 'none';
  	var info = $(this).find("li");
  	info.each(function() {
  		if($(this).text().substring(0,4) === 'Set:') {
  			 text = $(this).text().replace('Set:', '');
  		}
  	});
  	return text;
  },
  race: function() {
  	var text = 'none';
  	var info = $(this).find("li");
  	info.each(function() {
  		if($(this).text().substring(0,5) === 'Race:') {
  			 text = $(this).text().replace('Race:', '');
  		}
  	});
  	return text;
  },
  faction: function() {
  	var text = 'none';
  	var info = $(this).find("li");
  	info.each(function() {
  		if($(this).text().substring(0,8) === 'Faction:') {
  			 text = $(this).text().replace('Faction:', '');
  		}
  	});
  	return text;
  },
  cost: function() {
  	var text = 'none';
  	var info = $(this).find("li");
  	info.each(function() {
  		if($(this).text().substring(0,14) === 'Crafting Cost:') {
  			 text = $(this).text().replace('Crafting Cost:', '');
  		}
  	});
  	return text;
  },
  dust: function() {
  	var text = 'none';
  	var info = $(this).find("li");
  	info.each(function() {
  		if($(this).text().substring(0,19) === 'Arcane Dust Gained:') {
  			 text = $(this).text().replace('Arcane Dust Gained:', '');
  		}
  	});
  	return text;
  },
  artist: function() {
  	var text = 'none';
  	var info = $(this).find("li");
  	info.each(function() {
  		if($(this).text().substring(0,7) === 'Artist:') {
  			 text = $(this).text().replace('Artist:', '');
  		}
  	});
  	return text;
  }
}, artoo.savePrettyJson);