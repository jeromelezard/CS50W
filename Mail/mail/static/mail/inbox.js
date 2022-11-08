document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
 
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';


  // Clear out composition fields
 
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'flex';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(element => {
        const emailContainer = document.createElement('div');
        emailContainer.setAttribute('id', `${element.id}`);
        emailContainer.setAttribute('class', 'emailContainer');
        emailContainer.addEventListener('click', function() {
          fetch(`/emails/${element.id}`)
            .then(response => response.json())
            .then(email => {
              console.log(email);
              load_email(email, mailbox);
          });
        })
        document.querySelector('#emails-view').append(emailContainer);
        const sender = document.createElement('div');
        sender.setAttribute('id', `${element.id}`);
        const subject = document.createElement('div');
        subject.setAttribute('id', `${element.id}`);
        const date = document.createElement('div');
        date.setAttribute('id', `${element.id}`);
        
        if (mailbox == 'sent') {
          const recipient = element["recipients"][0];
          let length = element["recipients"].length;
          if (length == 1) {
            sender.innerHTML = `To: ${recipient}`;
          } else {
            sender.innerHTML = `To: ${recipient} (${length})`; 
          }
        } else {
          sender.innerHTML = element["sender"];
        }
        if (element.read === true && mailbox !== 'sent') {
          emailContainer.style.backgroundColor = '#ddd';
          
        }
        if (element.read === false){
          emailContainer.style.fontWeight = 'bold';

        }
        subject.innerHTML = element["subject"];
        date.innerHTML = element["timestamp"];
        emailContainer.append(sender);
        emailContainer.append(subject);
        emailContainer.append(date);
        
      });
      });
  }
function send_email(e) {
  e.preventDefault();
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');
  });
}


function load_email(email, mailbox) {
  // hide other pages
  
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  //show current email div
  const email_view = document.querySelector('#email-view');
  email_view.style.display= 'block';
  
  let user_id = document.querySelector('#userId').value;
  if (user_id === email.sender) {
    var sender = "You";
  } else {
    var sender = email.sender;
  }
  // mark emails as read if unread and opened from inbox
  if (mailbox === 'inbox' && email.read === false) {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });
  }
  //create template
  email_view.innerHTML = `<p><strong>From: </strong>${sender}</p><p><strong>To: </strong>${email.recipients}</p>
  <p><strong>Subject: </strong>${email.subject}</p><p><strong>Timestamp: </strong>${email.timestamp}</p>`;
  const reply = document.createElement('button');
  if (sender != "You") {
    reply.setAttribute('class', 'btn btn-sm btn-outline-primary');
    reply.setAttribute('id', 'reply');
    reply.innerHTML = "Reply";
    reply.addEventListener('click', function()  {
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      document.querySelector('#email-view').style.display = 'none';


  // Clear out composition fields
  
      document.querySelector('#compose-recipients').value = email.sender;
      if (email.subject.substring(0,3) == 'Re:') {
      document.querySelector('#compose-subject').value = `${email.subject}`;
      } else {

        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      }
      document.querySelector('#compose-body').value = `\n\n\nOn ${email.timestamp} ${email.sender} wrote '${email.body}'\n\n\n`;
    
      });
      email_view.append(reply);
    }
    if (email.archived === false) {
      const archive = document.createElement('button');
      archive.innerHTML = "Archive";
      archive.setAttribute('class', 'btn btn-sm btn-outline-primary');
      archive.setAttribute('id', 'archive');
      archive.addEventListener('click', function() {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: true
          })
        })
        .then(function() {
          document.querySelector('#archive').innerHTML = "Unarchive";
        });
      });

    email_view.append(archive);

    } else {
      const archive = document.createElement('button');
      archive.innerHTML = "Unarchive";
      archive.setAttribute('class', 'btn btn-sm btn-outline-primary');
      archive.setAttribute('id', 'archive');
      archive.addEventListener('click', function() {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: false
          })
        })
        .then(function() {
          document.querySelector('#archive').innerHTML = "Archive";
        });
      });

      email_view.append(archive);
    }
  
  email_view.append(document.createElement('hr'));
  const body = document.createElement('div');
  body.setAttribute('id', 'emailBody');
  body.innerHTML = email.body;
  email_view.append(body);
  
}
