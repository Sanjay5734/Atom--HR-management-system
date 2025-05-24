import React, { useState } from 'react';
import { FaStar, FaRegStar, FaTrashAlt, FaEdit, FaUserCircle } from 'react-icons/fa';

const ContactCard = ({ contact, onDelete, onToggleFavorite, onEdit }) => {
  return (
    <div className="bg-white p-5 rounded-2xl shadow-md hover:shadow-lg transition-all border border-gray-100">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <FaUserCircle className="text-4xl text-[#6936D6]" />
          <div>
            <h3 className="text-lg font-semibold text-gray-800">{contact.name}</h3>
            <p className="text-sm text-gray-500">{contact.email}</p>
            <p className="text-sm text-gray-400 italic">{contact.phone}</p>
            <p className="text-sm text-gray-400 italic">{contact.company}</p>
          </div>
        </div>
        <div className="flex items-center gap-4 text-[#6936D6] text-lg">
          <button onClick={() => onToggleFavorite(contact.id)}>
            {contact.favorite ? <FaStar /> : <FaRegStar />}
          </button>
          <button onClick={() => onEdit(contact.id)}><FaEdit /></button>
          <button onClick={() => onDelete(contact.id)}><FaTrashAlt /></button>
        </div>
      </div>
    </div>
  );
};

const Contacts = () => {
  const [contacts, setContacts] = useState([
    { id: 1, name: "Alice Smith", email: "alice@example.com", phone: "123-456-7890", company: "Tech Corp", favorite: false },
    { id: 2, name: "Bob Johnson", email: "bob@example.com", phone: "987-654-3210", company: "Webify Inc.", favorite: true },
    { id: 3, name: "Charlie Davis", email: "charlie@example.com", phone: "555-123-4567", company: "Design Co.", favorite: false },
    { id: 4, name: "Diana Prince", email: "diana@example.com", phone: "444-987-6543", company: "Hero Labs", favorite: true },
    { id: 5, name: "Evan Wright", email: "evan@example.com", phone: "321-654-0987", company: "NextGen Tech", favorite: false },
    { id: 6, name: "Fiona Green", email: "fiona@example.com", phone: "222-333-4444", company: "Green Solutions", favorite: false },
    { id: 7, name: "George King", email: "george@example.com", phone: "111-222-3333", company: "Royal Innovations", favorite: true },
    { id: 8, name: "Hannah Lee", email: "hannah@example.com", phone: "999-888-7777", company: "CloudNest", favorite: false },
    { id: 9, name: "Ian Black", email: "ian@example.com", phone: "777-666-5555", company: "SecureTech", favorite: true }
  ]);

  const handleDelete = (id) => {
    setContacts(contacts.filter(contact => contact.id !== id));
  };

  const handleToggleFavorite = (id) => {
    setContacts(contacts.map(contact =>
      contact.id === id ? { ...contact, favorite: !contact.favorite } : contact
    ));
  };

  const handleEdit = (id) => {
    const name = prompt("Edit name:");
    if (name) {
      setContacts(contacts.map(contact =>
        contact.id === id ? { ...contact, name } : contact
      ));
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 bg-gradient-to-r from-[#6936D6] to-[#152A65] bg-clip-text text-transparent text-center">My Contacts</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {contacts.map(contact => (
          <ContactCard
            key={contact.id}
            contact={contact}
            onDelete={handleDelete}
            onToggleFavorite={handleToggleFavorite}
            onEdit={handleEdit}
          />
        ))}
      </div>
    </div>
  );
};

export default Contacts;
