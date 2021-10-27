import React from 'react';
import './logoutlink.css';
import { Link } from "react-router-dom";

interface LogoutLinkProps {
  /**
   * Patient ID
   */
  name: string;
}

/**
 * Link to individual Patient 
 */
const LogoutLink = ({ name }: LogoutLinkProps) => {
  return (
    <div className="float-end">Logged in: { name }, <Link to="/logout">Logout</Link></div>
  );
};

export default LogoutLink;