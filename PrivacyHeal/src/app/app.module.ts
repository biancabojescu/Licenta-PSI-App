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


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    AngularFireModule.initializeApp(environment.firebaseConfig),
    AngularFirestoreModule,
    MaterialModule,
    SidebarComponent,
    LoginComponent,
    HomeComponent,
    MatInputModule,
    ReactiveFormsModule,
    FormsModule,
    MatMenuModule,
    MatAutocompleteModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
