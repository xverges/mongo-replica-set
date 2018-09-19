# -*- mode: ruby -*-
# vi: set ft=ruby :


(ENV['FIRST_IP'] &&
 ENV['FIRST_PORT'] &&
 ENV['SECOND_IP'] &&
 ENV['SECOND_PORT'] &&
 ENV['ARBITRER_IP'] &&
 ENV['ARBITRER_PORT'] &&
 ENV['REPLICASET_NAME']) || raise('Missing required environment variables. Use "pipenv shell" or https://gist.github.com/judy2k/7656bfe3b322d669ef75364a46327836')


$key_file = __dir__ + "/docker/key-file"
if !File.exist?($key_file)
    system("openssl rand -base64 756 > " + $key_file)
end


servers=[
  {
    :hostname => "first",
    :ip => "192.168.100.10",
    :hostport => 27110
  },
  {
    :hostname => "second",
    :ip => "192.168.100.11",
    :hostport => 27111
  },
  {
    :hostname => "arbitrer",
    :ip => "192.168.100.12",
    :hostport => 27112
  }
]


Vagrant.configure(2) do |config|
    
    config.vm.box = "bento/centos-7.3"

    servers.each do |machine|
        config.vm.define machine[:hostname], autostart: false do |node|

            hostname = machine[:hostname]

            puts "Working with " + hostname + "... Mapped to the host port " + machine[:hostport].to_s

            node.vm.hostname = machine[:hostname]
            node.vm.network "private_network", ip: machine[:ip]
            node.vm.network "forwarded_port", guest: 27017, host: machine[:hostport]

            node.vm.provider "virtualbox" do |virtualbox|
              # Allow (unsuccesfully) the second adapter (the one on the private_network), to accept connections from the host)
              # The allow-all flags is set, but did not fix the issue
              virtualbox.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
            end

            system("/usr/local/opt/gettext/bin/envsubst < "+
                   __dir__ + "/docker/docker-compose.template.yml > " +
                   __dir__ + "/docker/docker-compose." + hostname + ".yml")


            system("REPLICA_SET_PARAM='--bind_ip 0.0.0.0 --replSet " + ENV['REPLICASET_NAME'] + "' /usr/local/opt/gettext/bin/envsubst < "+
                   __dir__ + "/docker/docker-compose.template.yml > " +
                   __dir__ + "/docker/docker-compose." + hostname + "-repl.yml")



            node.vm.provision :docker
            node.vm.provision "shell",
                              privileged: false,
                              inline: <<-SHELL
                                mkdir -p /home/vagrant/mongo-secrets
                                sudo cp /vagrant/docker/key-file /home/vagrant/mongo-secrets/
                                sudo chown 999:999 /home/vagrant/mongo-secrets/key-file
                                sudo chmod 400 /home/vagrant/mongo-secrets/key-file
            SHELL
            if hostname != 'arbitrer'
              node.vm.provision :docker_compose, rebuild: true, run: "always", yml: "/vagrant/docker/docker-compose." + hostname + ".yml"
            end
        end
    end
end

