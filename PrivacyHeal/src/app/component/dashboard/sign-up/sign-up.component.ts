import { Component } from '@angular/core';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent {
  name: string | undefined;
  surname: string | undefined;
  gender: string | undefined;
  email: string | undefined;
  password: string | undefined;

  onSubmit() {
    console.log('Registration form submitted!');
    console.log(`Name: ${this.name}`);
    console.log(`Surname: ${this.surname}`)
    console.log(`Email: ${this.email}`);
    console.log(`Password: ${this.password}`);
  }
}
