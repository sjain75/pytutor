import {
  IonContent,
  IonIcon,
  IonItem,
  IonLabel,
  IonList,
  IonListHeader,
  IonMenu,
  IonMenuToggle,
  IonNote,
} from '@ionic/react';

import React from 'react';
import { useLocation } from 'react-router-dom';
import {calendarOutline, calendarSharp, clipboardOutline, clipboardSharp, codeOutline, codeSharp, helpOutline, helpSharp, bookmarkOutline, buildOutline, buildSharp} from 'ionicons/icons';
import './Menu.css';

interface AppPage {
  url: string;
  iosIcon: string;
  mdIcon: string;
  title: string;
}

const appPages: AppPage[] = [
  {
    title: 'Schedule',
    url: '/page/Schedule',
    iosIcon: calendarOutline,
    mdIcon: calendarSharp
  },
  {
    title: 'Syllabus',
    url: '/page/Syllabus',
    iosIcon: clipboardOutline,
    mdIcon: clipboardSharp
  },
  {
    title: 'Projects',
    url: '/page/Projects',
    iosIcon: codeOutline,
    mdIcon: codeSharp
  },
  {
    title: 'Resources',
    url: '/page/Resources',
    iosIcon: helpOutline,
    mdIcon: helpSharp
  },
  {
    title: 'Tools',
    url: '/page/Tools',
    iosIcon: buildOutline,
    mdIcon: buildSharp
  },
];

const labels = ['Function Scope'];

const Menu: React.FC = () => {
  const location = useLocation();

  return (
    <IonMenu contentId="main" type="overlay">
      <IonContent>
        <IonList id="inbox-list">
          <IonListHeader>pytutor</IonListHeader>
          <IonNote>Data Programming I</IonNote>
          {appPages.map((appPage, index) => {
            return (
              <IonMenuToggle key={index} autoHide={false}>
                <IonItem className={location.pathname === appPage.url ? 'selected' : ''} routerLink={appPage.url} routerDirection="none" lines="none" detail={false}>
                  <IonIcon slot="start" icon={appPage.iosIcon} />
                  <IonLabel>{appPage.title}</IonLabel>
                </IonItem>
              </IonMenuToggle>
            );
          })}
        </IonList>

        <IonList id="labels-list">
          <IonListHeader>Bookmarks</IonListHeader>
          {labels.map((label, index) => (
            <IonItem lines="none" key={index}>
              <IonIcon slot="start" icon={bookmarkOutline} />
              <IonLabel>{label}</IonLabel>
            </IonItem>
          ))}
        </IonList>
      </IonContent>
    </IonMenu>
  );
};

export default Menu;
