/* eslint-disable react/jsx-props-no-spreading */
import React, { useContext } from 'react';
import Notification from 'components/Notification';
import { AuthContext, PathwayContext } from 'app/context';
import './pagelayout.css';
import SdHeader from './SdHeader';
import SdFooter from './SdFooter';

export interface PageLayoutProps {
    children?: JSX.Element
}

/**
 * This component takes an element and returns the element with
 * a Header above and a Footer below.
 */
const PageLayout = ({
  children,
}: PageLayoutProps): JSX.Element => {
  const { user } = useContext(AuthContext);
  const { updateCurrentPathwayId } = useContext(PathwayContext);
  const { currentPathwayId } = useContext(PathwayContext);
  const actualCurrentPathwayId = currentPathwayId || user?.pathways?.[0].id;
  return (
    <div>
      <SdHeader
        currentPathwayId={ actualCurrentPathwayId }
        pathwayOnItemSelect={ (pathwayId) => updateCurrentPathwayId(pathwayId) }
        searchOnSubmit={ () => console.log('search submit') }
        user={ user }
      />
      {children}
      <SdFooter />
      {/* <Notification /> */}
    </div>
  );
};

export default PageLayout;
