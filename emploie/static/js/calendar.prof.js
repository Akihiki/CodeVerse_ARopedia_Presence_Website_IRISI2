
/**
 * EQUIPE  : CODEVERSE
 * @author : KANNOUFA FATIMA EZZAHRA
 *  
 */


// récupérer l'id du professeur connecté
idProf= $("#idProf").val();

window.onload = MyCalendar(idProf);

async function MyCalendar(idProf) {
  let data = await getSeances(idProf);
  drawCalendar(data.map( seance => {
      random_color = getRandomColor()
      return {
          title: seance.planning.libelle,
          start: dateFormat(seance.date),
          description: seance.planning.groupe.niveau.nom_niveau,
          url: "/emploie/liste-presence/" + string_to_slug(seance.planning.libelle + '-' +seance.date) + "/" + seance.id,
          color: random_color["color"],
          textColor: random_color["textColor"],
          display: 'block',
      }
  }))
}


function drawCalendar(data){
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {

        initialView: 'dayGridMonth',
        timeZone: 'local', 
        locale: 'fr',

        defaultAllDay: false,
        firstDay: 1,
  
        eventTimeFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: 'long'
        },
                  
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
            
        buttonText: {
          today:    'Aujourd\'hui',
          month:    'Mois',
          week:     'Semaines',
          day:      'Jour',
        },
                    
        events:  data,

    });

    
  
    calendar.render();
}

// récupérer les séances du professeur connecté
async function getSeances(idProf) {
  let url = '/emploie/api/prof/'+ idProf + '/seances';

  try {
      let data = await fetch(url);
      response = data.json()
      console.log(response)

      return await response;

  } catch (error) {
      console.log('Il y a eu un problème avec l\'opération fetch: ' + error.message);
  }
}


/**
 * Fonctions utiles
 */

//  transformer une chaine de caractère en slug
function string_to_slug (str) {
  str = str.replace(/^\s+|\s+$/g, '');
  str = str.toLowerCase();

  var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
  var to   = "aaaaeeeeiiiioooouuuunc------";
  for (var i=0, l=from.length ; i<l ; i++) {
      str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
  }

  str = str.replace(/[^a-z0-9 -]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-');

  return str;
}


//  Modifier le format du date (Format retourné : yyyy-mm-dd)
function dateFormat(myDate) {
  const date = new Date(myDate);

  const day = date.getDate();
  const month = date.getMonth() + 1;
  const year = date.getFullYear();    

  return year.toString() + "-" + month.toString().padStart(2,"0") + "-" +day.toString().padStart(2,"0");
}
 

//  retourner une couleur aléatoire
function getRandomColor(){
  random_color = colors[Math.floor(Math.random() * colors.length)]
  return random_color
}

 var colors = [
  {
    "color": "#E3E7F1",
    "textColor": "#494CA2"
  },
  {
    "color": "#FEF7DC",
    "textColor": "#A19882"
  },
  {
    "color": "#E9EFC0",
    "textColor": "#4E944F"
  },
  {
    "color": "#E9D5DA",
    "textColor": "#363062"
  },
  {
    "color": "#FDEBF7",
    "textColor": "#7A0BC0"
  },
  {
    "color": "#FED2AA",
    "textColor": "#C36A2D"
  },
  {
    "color": "#FDD2BF",
    "textColor": "#B61919"
  },
]