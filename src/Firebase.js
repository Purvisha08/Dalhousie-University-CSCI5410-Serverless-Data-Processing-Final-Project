import firebase from 'firebase/compat/app';
import 'firebase/compat/firestore';

const firebaseConfig = {
  apiKey: "AIzaSyB2LzCRmAyZR2VpEeHJp0cb2LXCUqECv6w",
  authDomain: "serverless-project-370320.firebaseapp.com",
  projectId: "serverless-project-370320",
  storageBucket: "serverless-project-370320.appspot.com",
  messagingSenderId: "1018129956430",
  appId: "1:1018129956430:web:b985cda325facbf0b8cd1f"
};
  const firebaseApp = firebase.initializeApp(firebaseConfig);

  export default firebaseApp;
