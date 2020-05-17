<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Klausurdatenbank</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.exam-modal>
Klausur hinzufügen</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Charakterisierung</th>
              <th scope="col">Stand</th>
              <th scope="col">Niveau</th>
              <th scope="col">Sachverhalt</th>
              <th scope="col">Lösung</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(exam, index) in exams" :key="index">
              <td>{{ exam.character }}</td>
              <td>{{ exam.date }}</td>
              <td>{{ exam.niveau }}</td>
              <td>{{ exam.case }}</td>
              <td>{{ exam.solution }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Aktualisieren</button>
                  <button type="button" class="btn btn-danger btn-sm">Löschen</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>


<b-modal ref="addExamModal"
         id="exam-modal"
         title="Neue Klausur hinzufügen"
         hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
  <b-form-group id="form-character-group"
                label="Charakterisierung:"
                label-for="form-character-input">
      <b-form-input id="form-character-input"
                    type="text"
                    v-model="addExamForm.character"
                    required
                    placeholder="Fügen Sie die Klausur-Charakterisierung hinzu">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-date-group"
                  label="Stand:"
                  label-for="form-date-input">
        <b-form-input id="form-date-input"
                      type="text"
                      v-model="addExamForm.date"
                      required
                      placeholder="Fügen Sie hier ein Datum ein">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-niveau-group"
                  label="Niveau:"
                  label-for="form-niveau-input">
        <b-form-input id="form-niveau-input"
                      type="text"
                      v-model="addExamForm.niveau"
                      required
                      placeholder="Fügen Sie hier ein Niveau ein">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-case-group"
                  label="Sachverhalt:"
                  label-for="form-case-input">
        <b-form-input id="form-case-input"
                      type="text"
                      v-model="addExamForm.case"
                      required
                      placeholder="Fügen Sie hier einen Link zum Sachverhalt ein">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-solution-group"
                  label="Lösungsskizze:"
                  label-for="form-solution-input">
        <b-form-input id="form-solution-input"
                      type="text"
                      v-model="addExamForm.solution"
                      required
                      placeholder="Fügen Sie hier einen Link zur Lösungsskizze ein">
        </b-form-input>
      </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>


  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      exams: [],
      addExamForm: {
        character: '',
        date: '',
        niveau: '',
        case: '',
        solution: '',
      },
    };
  },
  methods: {
    getExams() {
      const path = 'http://localhost:5000/exams';
      axios.get(path)
        .then((res) => {
          this.exams = res.data.exams;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addExam(payload) {
      const path = 'http://localhost:5000/exams';
      axios.post(path, payload)
        .then(() => {
          this.getExams();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getExams();
        });
    },
    initForm() {
      this.addExamForm.character = '';
      this.addExamForm.date = '';
      this.addExamForm.niveau = '';
      this.addExamForm.case = '';
      this.addExamForm.solution = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addExamModal.hide();
      const payload = {
        character: this.addExamForm.character,
        date: this.addExamForm.date,
        niveau: this.addExamForm.niveau,
        case: this.addExamForm.case,
        solution: this.addExamForm.solution,
      };
      this.addExam(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addExamModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getExams();
  },
};
</script>

/* eslint-disable eol-last */
