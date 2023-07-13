<template>
    <div>
      <FullCalendar
        :events="events"
        :options="calendarOptions"
      />
    </div>
  </template>

  <script>
  import { FullCalendar } from '@fullcalendar/vue3';
  import dayGridPlugin from '@fullcalendar/daygrid';
  import interactionPlugin from '@fullcalendar/interaction';

  export default {
    components: {
      FullCalendar,
    },
    data() {
      return {
        events: [], // Tableau pour stocker les événements
        calendarOptions: {
          plugins: [dayGridPlugin, interactionPlugin],
          initialView: 'dayGridMonth',
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay',
          },
          editable: true, // Activer le déplacement et le redimensionnement des événements
          selectable: true, // Activer la sélection de dates pour créer de nouveaux événements
          eventClick: this.handleEventClick, // Gérer le clic sur un événement
          dateClick: this.handleDateClick, // Gérer le clic sur une date
        },
      };
    },
    mounted() {
      this.getEvents();
    },
    methods: {
      async getEvents() {
        // Faites une requête HTTP GET pour récupérer les événements depuis le backend Django
        try {
          const response = await axios.get('http://localhost:8000/api/event/events/');
          this.events = response.data;
        } catch (error) {
          console.log(error);
        }
      },
      handleEventClick(info) {
        // Gérer le clic sur un événement existant
        // Vous pouvez ouvrir une modal pour afficher les détails de l'événement ou effectuer d'autres actions
        console.log('Event clicked:', info.event);
      },
      handleDateClick(info) {
        // Gérer le clic sur une date vide pour créer un nouvel événement
        // Vous pouvez ouvrir une modal pour saisir les informations de l'événement ou effectuer d'autres actions
        console.log('Date clicked:', info.dateStr);
      },
    },
  };
  </script>

  <style>
  /* Ajoutez des styles CSS personnalisés pour le calendrier ici si nécessaire */
  </style>
