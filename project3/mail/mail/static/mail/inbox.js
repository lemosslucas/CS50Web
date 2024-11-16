document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', send_email);
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';  
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  document.querySelector('#emails-details-view').style.display = 'none';
  document.querySelector('#emails-details-view').innerHTML = '';

  get_email(mailbox)
}

function send_email(event) {
  event.preventDefault();
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value,
        read: false
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent')
  });
}

function get_email(mailbox) {
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails)
    emails.forEach(email => {
      const div_email = document.createElement('div');

      if (email.read == false) {
        div_email.innerHTML = `
        <h5><b>${email.sender}</b></h5>
        <h6><b>${email.subject}</b></h6> 
        <h6>${email.timestamp}</h6>`;
        div_email.className = 'list-group-item'
      } else {
        div_email.innerHTML = `
        <h5>${email.sender}</h5>
        <h6>${email.subject}</h6> 
        <h6>${email.timestamp}</h6>`;
        div_email.className = 'list-group-item list-group-item-dark'
      }

      div_email.addEventListener('click', () => view_email(email.id))

      document.querySelector('#emails-view').append(div_email)
    });
  })

}

function view_email(id_email) {
  fetch(`/emails/${id_email}`)
  .then(response => response.json())
  .then(email => {
    console.log(email)

    document.querySelector('#emails-view').style.display = 'none'
    document.querySelector('#compose-view').style.display = 'none'
    document.querySelector('#emails-details-view').style.display = 'block'
    
    document.querySelector('#emails-details-view').innerHTML = `
    <ul>
      <li class="list-group-item"><b>From:</b> ${email.sender}</li>
      <li class="list-group-item"><b>To:</b> ${email.recipients}</li>
      <li class="list-group-item"><b>Subject:</b> ${email.subject}</li>
      <li class="list-group-item">${email.timestamp}</li>
      <li class="list-group-item">${email.body}</li>
    </ul>`
    
    //atualiza o valor bool
    if(email.read == false) {
      fetch(`/emails/${id_email}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
        })
      })
    }
    
    archive_email(email)
    replay_email(email)
  })
}

function archive_email(email) {
  const archive_button = document.createElement('button')

  if (email.archived) {
    archive_button.innerHTML = 'Un Archive'
    archive_button.className = 'btn btn-success'
  } else {
    archive_button.innerHTML = 'Archive'
    archive_button.className = 'btn btn-secondary';
  }

  archive_button.addEventListener('click', function() {
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
      })
    })
    .then(() => {
      load_mailbox('inbox')
    })
  })  
  document.querySelector('#emails-details-view').append(archive_button)
}

function replay_email(email) {
  const replay_button = document.createElement('button')
  replay_button.className = 'btn btn-primary';
  replay_button.innerHTML = 'Replay'  

  replay_button.addEventListener('click', () => {
    compose_email()

    document.querySelector('#compose-recipients').value = email.sender
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`
  })

  document.querySelector('#emails-details-view').append(replay_button)
}