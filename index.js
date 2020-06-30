import express from 'express';
import fs from 'fs-extra';
import path from 'path';
import fileUpload from 'express-fileupload';
import childProcess from 'child_process';



const app =express();
const port =3400;


app.use(fileUpload());
app.post('/TosBuild',(req,res)=>{
   
    
    let uploadFiles  = req.files.targetFile;
    const fileName = req.files.targetFile.name;
    const dotIndex = fileName.indexOf('.');
    const appName = fileName.substr(0,dotIndex);
    console.log(fileName);
    const targetPath = path.join(__dirname,appName);

    if(fs.existsSync(path.join(__dirname,fileName))){
        fs.removeSync(path.join(__dirname,fileName));
    }
    if(fs.existsSync(targetPath)){
        fs.removeSync(targetPath);
    }
    uploadFiles.mv(path.join(__dirname,fileName),()=>{
        const cp = childProcess.spawn(
            'unzip',
            [
                path.join(__dirname, fileName), "-d" ,"./"+appName
            ],
            { cwd : path.join(__dirname), shell: true,  detached: true }
        );
    
        cp.on('exit',()=>{
            childProcess.spawn ('python3', [path.join(__dirname, 'make-cop-package-tmaxos.py'), '-tc', '--resource', path.join(__dirname,appName)],
                        {  cwd : __dirname, shell: true,  detached: true });
                       let stdOut = '';
                        cp.stdout.on('data', data => {
                           stdOut += data;
                           console.log(stdOut); 
                       });
                       cp.on('exit', () => {
                           res.sendFile( path.join(__dirname, 'COPApp.tai'));
                        });
        });
    });
    
    
});

app.listen(port, ()=>console.log('Tos build service is listening'));
