document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // submit handler
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';

  // if reply, get value

  // if create new email Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function email_view(email_id) {

  // console.log(email_id);

  // get single email
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Print email
      console.log(email);

      // Hide both existed div
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';

      // hide list of emails and display clicked email's detail
      const single_email_view = document.querySelector('#single-email-view');
      single_email_view.style.display = 'block';
      single_email_view.innerHTML = `
      <h5><strong>From:</strong> ${email.sender}</h5>
      <h5><strong>To:</strong> ${email.recipients}</h5>
      <h5><strong>Subject:</strong> ${email.subject}</h5>
      <h5><strong>Timestamp:</strong> ${email.timestamp}</h5>
      <hr>
      <p>${email.body}</p>
      `;

      // send a PUT request to update whether an email is read or not
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });

      // reply
      const reply_btn = document.createElement('button');
      reply_btn.innerHTML = '<i class="fa-solid fa-reply"></i> Reply';
      reply_btn.className = 'btn btn-outline-primary me-2';
      reply_btn.addEventListener('click', function () {
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;
        let subject = email.subject;
        if (subject.slice(0, 3) != 'Re:') {
          subject = 'Re: ' + email.subject;
        }
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
      });
      document.querySelector('#single-email-view').append(reply_btn);


      // Archive/ Unarchive logic
      const btn = document.createElement('button');
      btn.innerHTML = email.archived ? '<i class="fa-solid fa-arrow-up-from-bracket"></i> Unarchive' : '<i class="fa-solid fa-box-archive"></i> Archive';
      btn.className = email.archived ? 'btn btn-warning' : 'btn btn-success';
      btn.addEventListener('click', () => {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
        })
          .then(() => { load_mailbox('inbox'); });
      });
      document.querySelector('#single-email-view').append(btn);

    });
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the emails for that mailbox and user
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      if (emails.length > 0) {
        console.log(emails);
        // Loop through emails and create a div for each
        emails.forEach(singleEmail => {

          // console.log(singleEmail);

          // Create div for each email
          const newEmail = document.createElement('div');
          const ul = document.createElement('ul')
          newEmail.innerHTML = `
          <h6>${singleEmail.sender}</h6>
          <h6>${singleEmail.subject}</h6>
          <small>${singleEmail.timestamp}</small>
          `;

          // Change background-color
          newEmail.className = singleEmail.read ? 'bg-secondary-subtle border border-secondary p-2 mb-2 rounded-4' : 'bg-white border border-secondary p-2 mb-2 rounded-4';

          // Add click event to view email
          newEmail.addEventListener('click', function () {
            email_view(singleEmail.id);
          });

          document.querySelector('#emails-view').append(newEmail);
        });
      } else {
        console.log('there is no object');

        const element = document.createElement('div');
        element.className = 'alert alert-dark';
        element.innerHTML = '<i class="fa-solid fa-envelope"></i> No email(s) in this view';
        document.querySelector('#emails-view').append(element);
      }


    });
}

function send_email(event) {
  event.preventDefault();

  // Store fields
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // send data
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
    });
}


