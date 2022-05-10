import React from 'react';
import { gql, useQuery } from '@apollo/client';
import AdminUserForm, { GET_ROLES_FRAGMENT } from './components/AdminUserForm';
import { userAdminGetRoles } from './__generated__/userAdminGetRoles';

export const USER_ADMIN_GET_ROLES_QUERY = gql`
  ${GET_ROLES_FRAGMENT}
  query userAdminGetRoles {
    getRoles {
      ...RoleParts
    }
  }
`;

export const AdminUserCreate = (): JSX.Element => {
  const { data } = useQuery<userAdminGetRoles>(USER_ADMIN_GET_ROLES_QUERY);
  return <AdminUserForm roles={ data?.getRoles } />;
};