<template>
    <div class="backend-content" id="content">
        <div class="column col-8 col-xs-12">
          <h3 class="s-title">Gérer les éléments whitelist</h3>
          <ul class="tab tab-block">
            <li class="tab-item">
                <a href="#" v-on:click="switch_tab('bulk')" v-bind:class="{ active: tabs.bulk }">Importer un élément soit-même</a>
            </li>
            <li class="tab-item">
                <a href="#" v-on:click="switch_tab('file')" v-bind:class="{ active: tabs.file }">Importer depuis un fichier</a>
            </li>
            <li class="tab-item">
                <a href="#" v-on:click="switch_tab('export')" v-bind:class="{ active: tabs.export }">Exporter les éléments</a>
            </li>
          </ul>
          <div v-if="tabs.export">
            <iframe :src="export_url" class="frame-export"></iframe>
          </div>
          <div v-if="tabs.file">
            <label class="form-upload empty" for="upload">
                <input type="file" class="upload-field" id="upload" @change="import_from_file">
                <p class="empty-title h5">Drop ou sélectionne un fichier à importer.</p>
                <p class="empty-subtitle">Le fichier doit être un fichier whitelist exporté depuis une instance SpyGuard.</p>
            </label>
          </div>
          <div v-if="tabs.bulk">
            <div class="form-group">
                <select class="form-select width-full" placeholder="test" v-model="type">
                    <option value="">Type d'éléments</option>
                    <option value="unknown">Multiple (regex parsing)</option>
                    <option v-for="t in types" :value="t.type" :key="t.type">
                        {{ t.name }}
                    </option>
                </select>
            </div>
            <div class="form-group">
                <textarea class="form-input" id="input-example-3" placeholder="Paste the elements to be whitelisted here" rows="15" v-model="elements"></textarea>
            </div>
            <div class="form-group">
                <button class="btn-primary btn col-12" v-on:click="import_from_bulk()">Eléments whitelist</button>
            </div>
          </div>
          <div class="form-group" v-if="imported.length>0">
            <div class="toast toast-success">
                ✓ {{imported.length}} IOC<span v-if="errors.length>1">s</span> importé avec succès.
            </div>
          </div>
            <div v-if="errors.length>0">
                <div class="form-group">
                    <div class="toast toast-error">
                        ✗ {{errors.length}} IOC<span v-if="errors.length>1">s</span> pas importé, voir les détails en dessous.
                    </div>
                </div>
                <div class="form-group">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Elément</th>
                                <th>erreur d'importation</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="e in errors" :key="e.element">
                                <td>{{ e.element }}</td>
                                <td>{{ e.message }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-else-if="type_tag_error==true">
                <div  class="form-group">
                    <div class="toast toast-error">
                        ✗ IOC(s) pas importé, voir les détails en dessous.
                    </div>
                </div>
                <div  class="form-group">
                    <div class="empty">
                        <p class="empty-title h5">Veuillez sélectionner un tag et un type.</p>
                        <p class="empty-subtitle">Si différents types d'IOCs, veuillez sélectionner "Unknown (regex parsing)".</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'manageiocs',   
    data() {
        return { 
            type:"",
            elements:"",
            types:[],
            errors:[],
            imported:[],
            wrong_wh_file: false,
            tabs: { "bulk" : true, "file" : false, "export" : false },
            jwt:"",
            export_url:""
        }
    },
    props: { },
    methods: {
        import_from_bulk: function() {
            this.errors   = []
            this.imported = []
            if (this.type != ""){
                this.elements.match(/[^\r\n]+/g).forEach(elem => {
                    this.import_element(this.type, elem);
                });
                this.elements = "";
            } else {
                this.type_tag_error = true
            }
        },
        import_element: function(type, elem) {
            if (elem != "" && elem.slice(0,1)  != "#"){
                axios.get(`/api/whitelist/add/${type.trim()}/${elem.trim()}`, { 
                    timeout: 10000, 
                    headers: { "X-Token" : this.jwt } 
                }).then(response => {
                    if(response.data.status){
                        this.imported.push(response.data);
                    } else if (response.data.message){
                        this.errors.push(response.data);
                    }
                })
                .catch(err => (console.log(err)))
            }
        },
        enrich_types: function() {
            axios.get(`/api/whitelist/get/types`, { timeout: 10000, headers: {'X-Token': this.jwt} })
            .then(response => {
                if(response.data.types) this.types = response.data.types
            })
            .catch(err => (console.log(err)));
        },
        switch_tab: function(tab) {
            this.errors   = []
            this.imported = []

            Object.keys(this.tabs).forEach(key => {
                if( key == tab ){
                    this.tabs[key] = true
                } else {
                    this.tabs[key] = false
                }
            });
        },
        import_from_file: function(ev) {
            this.errors   = []
            this.imported = []
            
            const file = ev.target.files[0];
            const reader = new FileReader();

            reader.onload = e => this.$emit("load", e.target.result);
            reader.onload = () => {
                try {
                    JSON.parse(reader.result).elements.forEach(elem => {
                        this.import_element(elem["type"], elem["element"])
                    })
                } catch (error) {
                    this.wrong_wh_file = true
                }

            } 
            reader.readAsText(file);
        },
        async get_jwt(){
            await axios.get(`/api/get-token`, { timeout: 10000 })
                .then(response => {
                    if(response.data.token){
                        this.jwt = response.data.token
                    }
                })
            .catch(err => (console.log(err)))
        }
    },
    created: function() {
        this.get_jwt().then(() => {
           this.enrich_types(); 
           this.export_url = `/api/whitelist/export?token=${this.jwt}`
        });
    }
}
</script>