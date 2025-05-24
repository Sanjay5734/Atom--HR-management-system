import React, { useEffect, useState } from 'react';
import Email from './Email';
import useGetAllEmails from '../hooks/useGetAllEmails';
import { useSelector } from 'react-redux';

const Emails = () => {
  useGetAllEmails();

  const { emails, searchText } = useSelector((store) => store.app);
  const [filteredEmails, setFilteredEmails] = useState([]);

  useEffect(() => {
    if (emails?.length > 0) {
      const filtered = emails.filter((email) =>
        email.subject?.toLowerCase().includes(searchText.toLowerCase()) ||
        email.to?.toLowerCase().includes(searchText.toLowerCase()) ||
        email.body?.toLowerCase().includes(searchText.toLowerCase())
      );
      setFilteredEmails(filtered);
    } else {
      setFilteredEmails([]);
    }
  }, [searchText, emails]);

  return (
    <div className="p-2 space-y-2">
      {filteredEmails.length > 0 ? (
        filteredEmails.map((email) => (
          <div key={email._id} className="bg-white shadow-sm rounded-lg p-4 hover:shadow-md transition-all duration-200">
            <Email email={email} />
          </div>
        ))
      ) : (
        <p className="text-center text-gray-500 mt-10">No emails found.</p>
      )}
    </div>
  );
};

export default Emails;
