
/**
 * EQUIPE  : CODEVERSE
 * @author : KANNOUFA FATIMA EZZAHRA
 *  
 */

$("#changePresenceModal").on('show.bs.modal', 
function (event) {

    var btn = $(event.relatedTarget)

    var id_etudiant = btn.data('id_etudiant')
    var id_seance = btn.data('id_seance')
    var nom_etudiant = btn.data('nom_etudiant')

    $("#modifier_url").attr("href", "/emploie/modifier-presence/"+ id_seance + "/" + id_etudiant)
      
    var modal = $(this)
          
    modal.find('#msg_modal')
        .text("Voulez-vous vraiment modifier la présence de l'étudiant(e) : " + nom_etudiant)
})

