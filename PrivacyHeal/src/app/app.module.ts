import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AngularFireModule } from "@angular/fire/compat";
import { AngularFirestoreModule} from "@angular/fire/compat/firestore";

import {AppRoutingModule} from "./app-routing.module";
import { AppComponent } from './app.component';
import { BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {environment} from "../environments/environment";
import {MaterialModule} from "./material/material/material.module";
import {SidebarComponent} from "./component/dashboard/sidebar/sidebar.component";
import {LoginComponent} from "./component/dashboard/login/login.component";
import {HomeComponent} from "./component/dashboard/home/home.component";
import {MatAutocompleteModule} from '@angular/material/autocomplete'
import {MatInputModule} from "@angular/material/input";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";

import {MatMenuModule} from "@angular/material/menu";
import {SignUpComponent} from "./component/dashboard/sign-up/sign-up.component";
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatButtonModule} from "@angular/material/button";
import {MatListModule} from "@angular/material/list";
import {MatIconModule} from "@angular/material/icon";
import {AsyncPipe, NgOptimizedImage} from "@angular/common";
import {MatSidenavModule} from "@angular/material/sidenav";


@NgModule({
  declarations: [
    AppComponent,
    SidebarComponent,
    LoginComponent,
    HomeComponent,
    SignUpComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    AngularFireModule.initializeApp(environment.firebaseConfig),
    AngularFirestoreModule,
    MaterialModule,
    MatInputModule,
    ReactiveFormsModule,
    FormsModule,
    MatMenuModule,
    MatAutocompleteModule,
    MatToolbarModule,
    MatButtonModule,
    MatListModule,
    MatIconModule,
    AsyncPipe,
    NgOptimizedImage,
    MatSidenavModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
