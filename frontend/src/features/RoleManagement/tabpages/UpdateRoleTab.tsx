import React, { useEffect, useState } from 'react';
import * as yup from 'yup';
import { useFieldArray, useForm } from 'react-hook-form';
import { ApolloQueryResult, OperationVariables } from '@apollo/client';
import { yupResolver } from '@hookform/resolvers/yup';
import { Modal } from 'react-bootstrap';
import { Button, ErrorMessage, Fieldset, Form, SummaryList } from 'nhsuk-react-components';
import { Input, Select } from 'components//nhs-style';
import { getRoles } from 'features/RoleManagement/__generated__/getRoles';

type UpdateRoleForm = {
  name: string;
  roleIndex: string;
  permissions: {
    name: string;
    checked: boolean;
  }[];
};

export interface UpdateRoleInputs {
  name: string;
  roleIndex: string;
  permissions: { name: string; checked: boolean; }[];
}

export type UpdateRoleReturnData = {
  id: number,
  name: string,
  permissions: string[],
};

type UpdateRoleSubmitHook = [
  boolean,
  any,
  UpdateRoleReturnData | undefined,
  (variables: UpdateRoleInputs) => void
];

export function useUpdateRoleSubmit(
  setShowModal: (arg0: boolean) => void,
  refetchRoles?: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<getRoles>>,
): UpdateRoleSubmitHook {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<unknown>(undefined);
  const [data, setData] = useState<UpdateRoleReturnData | undefined>(undefined);

  async function updateRole(variables: UpdateRoleInputs) {
    setLoading(true);
    setData(undefined);
    setError(undefined);

    try {
      const { location } = window;
      const uriPrefix = `${location.protocol}//${location.host}`;

      const listOfPermissions = variables.permissions.filter(
        (perm) => (perm.checked !== false || null),
      ).map((value) => (value.name));

      const updateResponse = await window.fetch(`${uriPrefix}/api/rest/updaterole/`, {
        method: 'POST',
        headers: {
          'content-type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify({
          id: variables.roleIndex,
          name: variables.name,
          permissions: listOfPermissions,
        }),
      });
      if (!updateResponse.ok) {
        if (updateResponse.status === 409) {
          setError('Error: a role with this name already exists');
          throw new Error('Error: a role with this name already exists');
        } else {
          setError(`Error: Response ${updateResponse.status} ${updateResponse.statusText}`);
          throw new Error(`Error: Response ${updateResponse.status} ${updateResponse.statusText}`);
        }
      }
      const decodedResponse: UpdateRoleReturnData = await updateResponse.json();
      setData(decodedResponse);
      setShowModal(true);
      if (refetchRoles) {
        refetchRoles();
      }
    } catch (err) {
      setError(err);
      setData(undefined);
    }
    setLoading(false);
  }
  return [loading, error, data, updateRole];
}

export interface UpdateRoleTabProps {
  disableForm?: boolean | undefined,
  refetchRoles?: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<getRoles>>,
  roles?: {
    id: string;
    name: string;
    permissions: { name: string | undefined; }[];
  }[] | undefined
  rolePermissions?: {name: string}[],
}

const UpdateRoleTab = (
  { disableForm, refetchRoles, roles, rolePermissions }: UpdateRoleTabProps,
): JSX.Element => {
  const [showModal, setShowModal] = useState<boolean>(false);

  const [
    loading,
    error,
    data,
    updateRole,
  ] = useUpdateRoleSubmit(setShowModal, refetchRoles);

  const [selectedRole, setSelectedRole] = useState<string>('-1');

  const newRoleSchema = yup.object({
    name: yup.string().required('Role name is a required field'),
  }).required();

  const [
    permissionCheckboxesOrganised,
    setPermissionCheckboxesOrganised,
  ] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors: formErrors },
    getValues,
    setValue,
    control,
  } = useForm<UpdateRoleForm>({ resolver: yupResolver(newRoleSchema) });

  const {
    fields: permissionFields,
    append: appendPermissionFields,
  } = useFieldArray({
    name: 'permissions',
    control: control,
  });

  useEffect(() => {
    if (!permissionCheckboxesOrganised && rolePermissions) {
      const fieldProps: UpdateRoleForm['permissions'] = rolePermissions
        ? rolePermissions.flatMap((rolePermission) => (
          {
            name: rolePermission.name,
            checked: false,
          }
        ))
        : [];
      appendPermissionFields(fieldProps);
      setPermissionCheckboxesOrganised(true);
    }
  }, [
    rolePermissions,
    appendPermissionFields,
    permissionCheckboxesOrganised,
    setPermissionCheckboxesOrganised,
  ]);

  useEffect(() => {
    permissionFields?.forEach((permission, index) => {
      setValue(`permissions.${index}.checked`, false);
    });

    setValue('name', '');

    if (selectedRole !== '-1' && selectedRole) {
      permissionFields?.forEach((permission, index) => {
        setValue(`permissions.${index}.checked`, false);
      });

      const permissionSet = roles?.filter(
        (role) => (role.id === selectedRole),
      )?.[0];

      if (permissionSet) {
        setValue('name', permissionSet.name);
        permissionSet.permissions.forEach((rolePermission) => {
          if (rolePermission) {
            permissionFields.find((permission, index) => (
              permission.name === rolePermission.name
              && setValue(`permissions.${index}.checked`, true)
            ));
          }
        });
      }
    }
  }, [rolePermissions, roles, permissionFields, selectedRole, setValue]);

  return (
    <>
      { error ? <ErrorMessage>{error.message}</ErrorMessage> : null}
      <Form
        onSubmit={ handleSubmit( () => {
          updateRole(getValues());
        }) }
      >
        <Fieldset
          disabled={
            disableForm || loading || showModal
          }
        >
          <Select
            className="col-12"
            label="Select existing role"
            { ...register('roleIndex') }
            onChange={ (
              (e: { currentTarget: { value: React.SetStateAction<string> } }) => {
                setSelectedRole(e.currentTarget.value);
              }) }
          >
            <option value="-1">Select a role</option>
            {
              roles?.map((role) => (
                <option key={ role.id } value={ role.id }>{ role.name }</option>
              ))
            }
          </Select>
        </Fieldset>
        <Fieldset
          disabled={
            disableForm || loading || showModal
            || selectedRole === '-1'
          }
        >
          <Input role="textbox" id="name" label="Role name" error={ formErrors.name?.message } { ...register('name', { required: true }) } />
          <Fieldset.Legend>Role permissions</Fieldset.Legend>
          {
            permissionFields?.map((permission, index) => (
              <div className="form-check" key={ `permissions.${permission.name}.checked` }>
                <label className="form-check-label pull-right" htmlFor={ `permissions.${index}.checked` }>
                  <input
                    className="form-check-input"
                    type="checkbox"
                    value={ permission.name }
                    id={ `permissions.${index}.checked` }
                    { ...register(`permissions.${index}.checked` as const) }
                    defaultChecked={ false }
                  />
                  { permission.name }
                </label>
              </div>
            ))
          }
        </Fieldset>
        <Fieldset
          disabled={
            disableForm || loading || showModal
            || selectedRole === '-1'
          }
        >
          <Button
            type="submit"
            name="submitBtn"
            className="float-end"
          >
            Update role
          </Button>
        </Fieldset>
      </Form>
      <Modal show={ showModal } onHide={ (() => setShowModal(false)) }>
        <Modal.Header>
          <Modal.Title>Role updated</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <SummaryList>
            <SummaryList.Row>
              <SummaryList.Key>Role name</SummaryList.Key>
              <SummaryList.Value>{data?.name}</SummaryList.Value>
            </SummaryList.Row>
            <SummaryList.Row>
              <SummaryList.Key>Permissions</SummaryList.Key>
              <SummaryList.Value>
                <ul>
                  {
                    data?.permissions.map((name) => (
                      <li key={ `update_role_modal_perm_${name}` }>{name}</li>
                    ))
                  }
                </ul>
              </SummaryList.Value>
            </SummaryList.Row>
          </SummaryList>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={ (() => setShowModal(false)) }>Close</Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};
export default UpdateRoleTab;