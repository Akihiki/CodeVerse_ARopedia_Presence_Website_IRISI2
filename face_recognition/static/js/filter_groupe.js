/**
 * EQUIPE : CODEVERSE et AROPEDIA
 * @authors : + KANNOUFA F. EZZAHRA
 *            + MOUZAFIR ABDELHADI
 */

const Form = document.getElementById('modele-admin-form')

const FiliereDataBox = document.getElementById('filiere-data-box')
const NiveauDataBox = document.getElementById('niveau-data-box')
const GroupeDataBox = document.getElementById('groupe-data-box')

const FiliereInput = document.getElementById('filieres')
const NiveauInput = document.getElementById('niveaux')
const GroupeInput = document.getElementById('groupes')

const dropdownFilieres = document.getElementById('dropdownFilieres')
const dropdownNiveaux = document.getElementById('dropdownNiveaux')
const dropdownGroupes = document.getElementById('dropdownGroupes')

const btnBox = document.getElementById('btnBox')

// const dropdownanneeuniversitaire = document.getElementById('wikoid')
// dropdownanneeuniversitaire.addEventListener('click', e => {
//     console.log(e.target.value)
// })
$.ajax({
    type: 'GET',
    url: '/face-recognition/filieres-json/',
    success: function (response) {
        console.log(response.data)
        const filieresData = response.data
        filieresData.map(item => {
            const option = document.createElement('div')
            option.textContent = item.nom_filiere
            option.setAttribute('class', 'dropdown-item')
            option.setAttribute('id', item.nom_filiere)
            FiliereDataBox.appendChild(option)
        })

    },
    error: function (error) {
        console.log(error)
    }
})


var selectedFiliere
var selectedNiveau
var selectedGroupe

FiliereInput.addEventListener('click', e => {
    console.log(e.target.id)
    selectedFiliere = e.target.id


    btnBox.classList.add('disabled')


    NiveauDataBox.innerHTML = ""
    GroupeDataBox.innerHTML = ""
    dropdownFilieres.textContent = e.target.id

    dropdownNiveaux.textContent = "Filière"
    dropdownGroupes.textContent = "Groupe"


    $.ajax({
        type: 'GET',
        url: `/face-recognition/niveaux-json/${selectedFiliere}`,
        success: function (response) {
            console.log(response.data)
            const niveauxData = response.data
            niveauxData.map(item => {
                const option = document.createElement('div')
                option.textContent = item.nom_niveau
                option.setAttribute('class', 'dropdown-item')
                option.setAttribute('id', item.nom_niveau)
                NiveauDataBox.appendChild(option)
            })


            NiveauInput.addEventListener('click', e => {

                btnBox.classList.add('disabled')
                dropdownNiveaux.textContent = e.target.id
                dropdownGroupes.textContent = "Groupe"
                GroupeDataBox.innerHTML = ""
                console.log(e.target.id)
                selectedNiveau = e.target.id


                $.ajax({
                    type: 'GET',
                    url: `/face-recognition/groupes-json/${selectedNiveau}`,
                    success: function (response) {
                        console.log(response.data)
                        const groupesData = response.data
                        groupesData.map(item => {
                            const option = document.createElement('div')
                            option.textContent = item.nom_group
                            option.setAttribute('class', 'dropdown-item')
                            option.setAttribute('id', item.nom_group)
                            GroupeDataBox.appendChild(option)
                        })


                        GroupeInput.addEventListener('click', e => {
                            console.log(e.target.id)
                            selectedGroupe = e.target.id

                            dropdownGroupes.textContent = e.target.id
                            btnBox.classList.remove('disabled')

                            btnBox.setAttribute("href", `/face-recognition/training/${selectedFiliere}/${selectedNiveau}/${selectedGroupe}/`)
                            console.log("attr = " + btnBox)
                        })

                    },
                    error: function (error) {
                        console.log(error)
                    }
                })
            })


        },
        error: function (error) {
            console.log(error)
        }
    })

})

