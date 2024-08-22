import grpc
import headless_service_pb2_grpc
import headless_service_pb2
from functions import generate_guid, generate_random_balance
from global_vars import server


def add_or_update_headless_with_nous(nous_account_guid: str, club_guid: str, room_player_guid: str, gold_balance: int, chips_balance: int):
    with grpc.insecure_channel(server) as channel:
        stub = headless_service_pb2_grpc.HeadlessServiceStub(channel)
        request = headless_service_pb2.AddOrUpdateHeadlessRequest(
            club_guid=club_guid,
            room_player_guid=room_player_guid,
            gold_balance=gold_balance,
            chips_balance=chips_balance,
            nous_account_guid=nous_account_guid)
        try:
            response = stub.AddOrUpdateHeadless(request)
            return response
        except Exception as e:
            print(e)
            return "Error add_or_update_headless()"


def add_or_update_headless(club_guid: str, room_player_guid: str, gold_balance: int, chips_balance: int):
    nous_account_guid = generate_guid()
    with grpc.insecure_channel(server) as channel:
        stub = headless_service_pb2_grpc.HeadlessServiceStub(channel)
        request = headless_service_pb2.AddOrUpdateHeadlessRequest(
            club_guid=club_guid,
            room_player_guid=room_player_guid,
            gold_balance=gold_balance,
            chips_balance=chips_balance,
            nous_account_guid=nous_account_guid)
        try:
            response = stub.AddOrUpdateHeadless(request)
            return response
        except Exception as e:
            print(e)
            return "Error add_or_update_headless()"


def get_club_headlesses():
    club_headless = add_or_update_headless(generate_guid(), generate_guid(), 100, 50)
    with grpc.insecure_channel(server) as channel:
        stub = headless_service_pb2_grpc.HeadlessServiceStub(channel)
        request = headless_service_pb2.GetClubHeadlessesRequest(
            club_guid=club_headless.club_guid)
        try:
            response = stub.GetClubHeadlesses(request)
            return response
        except Exception as e:
            print(e)
            return "Error add_or_update_headless()"


def get_headless():
    club_headless = add_or_update_headless(generate_guid(), generate_guid(), 70, 999)
    with grpc.insecure_channel(server) as channel:
        stub = headless_service_pb2_grpc.HeadlessServiceStub(channel)
        request = headless_service_pb2.GetHeadlessRequest(
            nous_account_guid=club_headless.nous_account_guid,
            room_player_guid=club_headless.room_player_guid)
        try:
            response = stub.GetHeadless(request)
            return response
        except Exception as e:
            print(e)
            return "Error add_or_update_headless()"


if __name__ == "__main__":
    club_guid = generate_guid()
    for i in range(2):
        nous_account_guid = generate_guid()
        room_account_guid = generate_guid()
        gold_balance = generate_random_balance(-10,-1)
        chips_balance = generate_random_balance(-1000,-1)
        print(add_or_update_headless_with_nous(nous_account_guid, club_guid, room_account_guid, gold_balance, chips_balance))
       
