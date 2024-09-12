stage('Check new macOS') {
    node('built-in') {
        checkout scm
        sh "python3 -u macos_monitor.py"
        // Jenkins Push macos_version.db back to Git Repo
        sshagent (credentials: ['github']) {
            def changed = sh(script: "git diff macos_version.db", returnStdout: true).trim()
            if (changed) {
                sh """
                    git add macos_version.db
                    git commit -m "Jenkins Automatically Update macOS Version DB" || true
                    git push origin HEAD:main
                """
            } else {
                echo "No need to push back to Git"
            }
        }
    }
}