function toggleNotificationBox() {
    var notificationBox = document.getElementById("notificationBox");
    notificationBox.classList.toggle("show");
  }
  
  window.addEventListener("click", function(event) {
    var notificationBox = document.getElementById("notificationBox");
    var notificationIcon = document.getElementsByClassName("notification-icon")[0];
  
    if (!notificationIcon.contains(event.target) && !notificationBox.contains(event.target)) {
      notificationBox.classList.remove("show");
    }
  });
  

  function updateNotifications() {
    fetch('/get_notifications')
      .then(response => response.json())
      .then(data => {
        const notificationCount = data.notification_count;
        console.log(notificationCount);
        const notifications = data.notifications;
  
        // Update the notification count in the UI
        const notificationCountElement = document.getElementById('notificationCount');
        if (notificationCountElement) {
          notificationCountElement.textContent = notificationCount;
        }
  
        // Update the notifications list in the UI
        const notificationBox = document.getElementById('notificationBox');
        if (notificationBox) {
          notificationBox.innerHTML = ''; // Clear existing notifications
          const userId = notifications.length > 0 ? notifications[0].user_id : '';
          if (notifications.length > 0) {
            for (const notification of notifications) {
              const notificationItem = document.createElement('div');
              notificationItem.classList.add('notification-item');
              notificationItem.textContent = notification.body;
              notificationItem.appendChild(document.createElement('br'))
              senderUser = document.createElement('h4')
              senderUser.textContent = "By " + notification.sender_name
              console.log(notification.sender_name)
              notificationItem.appendChild(senderUser)
              if (notification.type === 'lb_request') {
                // Create Accept button
                
                const acceptButton = document.createElement('button');
                acceptButton.textContent = 'Accept';
                acceptButton.classList.add('notification-button');
                acceptButton.addEventListener('click', () => {
                  // Code to handle Accept button click

                  acceptNotification(notification.id,notification.user_id,notification.sender_name,notification.sender_id);
                });
                notificationItem.appendChild(acceptButton);
  
                // Create Decline button
                const declineButton = document.createElement('button');
                declineButton.textContent = 'Decline';
                declineButton.classList.add('notification-button');
                declineButton.addEventListener('click', () => {
                  // Code to handle Decline button click
                  declineNotification(notification.id,notification.user_id,notification.sender_name,notification.sender_id);
                });
                notificationItem.appendChild(declineButton);
              }
              const deleteNotificationButton = document.createElement('button');
              deleteNotificationButton.classList.add('trash-icon');
              deleteNotificationButton.setAttribute('aria-label', 'Trash');
              const icon = document.createElement('span');
              icon.classList.add('fa', 'fa-trash');
              deleteNotificationButton.appendChild(icon);

              deleteNotificationButton.addEventListener('click', () => {
                // Code to handle Delete Notification button click
                deleteNotification(notification.id);
              });
              notificationItem.appendChild(deleteNotificationButton);

              
              notificationBox.appendChild(notificationItem);
              
            }
              const deleteAllNotificationButton = document.createElement('button');
              deleteAllNotificationButton.textContent = "Clear";
              deleteAllNotificationButton.addEventListener('click', () => {
                // Code to handle Delete Notification button click
                deleteAllNotification(userId);
              });
            notificationBox.appendChild(deleteAllNotificationButton);
          } else {
            const noNotificationsMessage = document.createElement('div');
            noNotificationsMessage.textContent = 'No new notifications';
            notificationBox.appendChild(noNotificationsMessage);
          }
        }
      })
      .catch(error => {
        console.error('Error fetching notifications:', error);
      });
  }
  
  function startNotificationUpdates() {
    // Call updateNotifications() initially
    updateNotifications();
  
    // Schedule periodic updates using setInterval
    setInterval(updateNotifications, 5000); // Update every 5 seconds (adjust as needed)
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    startNotificationUpdates();
  });
  

  function createNotification(userId, body,type,sender_id) {
    fetch(`/create_notification/${userId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `body=${encodeURIComponent(body)}&type=${encodeURIComponent(type)}&sender_id=${encodeURIComponent(sender_id)}`, // Pass the notification body as form data
    })
      .then(response => response.text())
      .then(result => {
        console.log(result); // Notification created successfully
        // Optionally, you can trigger an update of the notifications list after creating the notification
        updateNotifications();
      })
      .catch(error => {
        console.error('Error creating notification:', error);
      });
  }
  
  function acceptNotification(notificationId,notified_user,sender_user,sender_id){


    fetch(`/accept_user_notification/${notificationId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `notified_user=${encodeURIComponent(notified_user)}&sender_user=${encodeURIComponent(sender_user)}`,
    })
      .then(response => response.text())
      .then(result => {
        console.log(result); // Notification created successfully
        // Optionally, you can trigger an update of the notifications list after creating the notification
        createNotification(sender_id,'Your Request Accepted!','ap_request',notified_user)
        
      })
      .catch(error => {
        console.error('Error creating notification:', error);
      });


  }


  function declineNotification(notificationId,notified_user,sender_user,sender_id){

    createNotification(sender_id,'Your Request Ignored!','ap_request',notified_user)
        

  }

  function deleteNotification(notificationId){
    fetch(`/delete_notification/${notificationId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: ``,
    })
      .then(response => response.text())
      .then(result => {
        console.log(result); // Notification created successfully
        // Optionally, you can trigger an update of the notifications list after creating the notification
        updateNotifications();
      })
      .catch(error => {
        console.error('Error creating notification:', error);
      });

  }


  function deleteAllNotification(userId){

    fetch(`/delete_all_notifications/${userId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: ``,
    })
      .then(response => response.text())
      .then(result => {
        console.log(result); // Notification created successfully
        // Optionally, you can trigger an update of the notifications list after creating the notification
        updateNotifications();
      })
      .catch(error => {
        console.error('Error creating notification:', error);
      });

  }